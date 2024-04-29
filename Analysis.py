from matplotlib import pyplot as plt
from predict import predict_sentiment
import csv
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from mycsv.csv import *


plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号 #有中文出现的情况，需要u'内容'




def read_csv_column(csv_file, column_name):
    """
    读取CSV文件指定列的数据并存储在列表中
    :param csv_file: CSV文件路径
    :param column_name: 指定列的列名
    :return: 包含指定列数据的列表
    """
    column_data = []  # 存储指定列的数据

    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if column_name in row:
                    column_data.append(row[column_name])
                else:
                    print(f"Column '{column_name}' not found in CSV file.")
                    return None
    except FileNotFoundError:
        print(f"File '{csv_file}' not found.")
        return None

    return column_data
def Analysis_tieba(csv_path, filename, column1_name, column2_name, column3_name, column4_name,column5_name):
    new_csv_path = f'TiebaAnalysis/{filename}.csv'
    column1_data, column2_data, column3_data, column4_data,column5_data = read_5columns_from_csv(csv_path, column1_name, column2_name, column3_name, column4_name,column5_name)
    if column1_data:
        for input_text, ip, agree, disagree,gender in zip(column1_data, column2_data, column3_data, column4_data,column5_data):
            print(input_text + ip)
            negative, positive = predict_sentiment(input_text, pad_size=50)
            write_to_csv_tieba(new_csv_path, input_text, negative, positive, agree, disagree,ip,gender)
    else:
        print("Failed to read column data.")
    return new_csv_path


def visualize_sentiments(csv_file):
    # 读取 CSV 文件
    df = pd.read_csv(csv_file)

    # 获取文件名（不包含后缀名）
    file_name = os.path.splitext(os.path.basename(csv_file))[0]

    # 将评论者性别映射为中文
    df['评论者性别'] = df['评论者性别'].map({'Gender.MALE': '男', 'Gender.FEMALE': '女', 'Gender.UNKNOWN': '未知'})

    # 根据省份和识别结果（消极、积极、中性）分组，并计算每个省份的评论数
    province_sentiments = df.groupby(['IP地址', '识别结果']).size().unstack(fill_value=0)

    # 创建子图布局，竖向排列
    fig = make_subplots(
        rows=6, cols=1,
        subplot_titles=('情绪评论比例', '各省份评论数统计', '情绪评论支持与反对', '男性情绪评论比例', '女性情绪评论比例', '未知性别情绪评论比例'),
        specs=[
            [{"type": "pie"}],
            [{"type": "bar"}],
            [{"type": "bar"}],
            [{"type": "pie"}],
            [{"type": "pie"}],
            [{"type": "pie"}]
        ],
        vertical_spacing=0.05
    )

    # 定义颜色方案
    colors = {'积极': '#2ca02c', '中性': '#1f77b4', '消极': '#d62728'}

    # 饼图数据准备 - 情绪评论比例
    overall_sentiments = df['识别结果'].value_counts()
    overall_sentiments = overall_sentiments.reindex(index=['积极', '中性', '消极'])

    # 饼状图 - 情绪评论比例
    fig.add_trace(
        go.Pie(labels=overall_sentiments.index, values=overall_sentiments, textinfo='label+percent', marker_colors=[colors[sentiment] for sentiment in overall_sentiments.index], name='情绪评论比例'),
        row=1, col=1
    )

    # 柱状图 - 各省份评论数统计
    for sentiment in ['积极', '中性', '消极']:
        fig.add_trace(
            go.Bar(x=province_sentiments.index, y=province_sentiments[sentiment], name='各省份评论数统计 - ' + sentiment, marker_color=colors[sentiment]),
            row=2, col=1
        )

    # 柱状图 - 情绪评论支持与反对
    support_oppose_sentiments = df.groupby('识别结果')[['支持', '反对']].sum().reindex(index=['积极', '中性', '消极'])
    print(support_oppose_sentiments)
    fig.add_trace(
        go.Bar(x=support_oppose_sentiments.index, y=support_oppose_sentiments['支持'], name='情绪评论支持与反对 - 支持', marker_color='#1f77b4'),
        row=3, col=1
    )
    fig.add_trace(
        go.Bar(x=support_oppose_sentiments.index, y=support_oppose_sentiments['反对'], name='情绪评论支持与反对 - 反对', marker_color='#d62728'),
        row=3, col=1
    )

    # 饼图数据准备 - 性别情绪评论比例
    gender_sentiments = df.groupby(['评论者性别', '识别结果']).size().unstack(fill_value=0)
    gender_sentiments_ratio = gender_sentiments.div(gender_sentiments.sum(axis=1), axis=0)

    # 男性情绪评论比例
    male_sentiments = gender_sentiments_ratio.loc['男']
    male_sentiments = male_sentiments.reindex(index=['积极', '中性', '消极'])
    fig.add_trace(
        go.Pie(labels=male_sentiments.index, values=male_sentiments, textinfo='label+percent', hole=0.3),
        row=4, col=1
    )

    # 女性情绪评论比例
    female_sentiments = gender_sentiments_ratio.loc['女']
    female_sentiments = female_sentiments.reindex(index=['积极', '中性', '消极'])
    fig.add_trace(
        go.Pie(labels=female_sentiments.index, values=female_sentiments, textinfo='label+percent', hole=0.3),
        row=5, col=1
    )

    # 未知性别情绪评论比例
    unknown_sentiments = gender_sentiments_ratio.loc['未知']
    unknown_sentiments = unknown_sentiments.reindex(index=['积极', '中性', '消极'])
    fig.add_trace(
        go.Pie(labels=unknown_sentiments.index, values=unknown_sentiments, textinfo='label+percent', hole=0.3),
        row=6, col=1
    )

    # 更新布局设置
    fig.update_layout(
        height=2400,  # 调整总图表高度
        showlegend=True,
        title_text=f"{file_name}分析报告",
        margin=dict(t=200),
        annotations=[
            dict(text="情绪评论比例", x=0.5, y=0.86, font=dict(size=12), showarrow=False, xref="paper", yref="paper", xanchor="center", yanchor="bottom"),
            dict(text="评论来源统计", x=0.5, y=0.68, font=dict(size=12), showarrow=False, xref="paper", yref="paper", xanchor="center", yanchor="bottom"),
            dict(text="情绪评论支持与反对", x=0.5, y=0.55, font=dict(size=12), showarrow=False, xref="paper", yref="paper", xanchor="center", yanchor="bottom"),
            dict(text="男性情绪评论比例", x=0.5, y=0.48, font=dict(size=12), showarrow=False, xref="paper", yref="paper", xanchor="center", yanchor="bottom"),
            dict(text="女性情绪评论比例", x=0.5, y=0.3, font=dict(size=12), showarrow=False, xref="paper", yref="paper", xanchor="center", yanchor="bottom"),
            dict(text="未知性别情绪评论比例", x=0.5, y=0.13, font=dict(size=12), showarrow=False, xref="paper", yref="paper", xanchor="center", yanchor="bottom"),
        ]
    )

    # 显示图表
    fig.show()

if __name__ == "__main__":
    # csv_path = "TieBaData/聊聊二次元遗老这个问题，非引战【bilibili吧】_百度贴吧.csv"
    # filename = "聊聊二次元遗老这个问题，非引战【bilibili吧】_百度贴吧.csv"
    # column1_name = "Text"
    # column2_name = "IP Address"
    # column3_name = "Agree"
    # column4_name = "Disagree"
    # column5_name = "Gender"
    # newfilepath = Analysis_tieba(csv_path, filename, column1_name, column2_name,column3_name,column4_name,column5_name)
    # app = QApplication([])
    # column_names = ['文本', '识别结果', '消极概率', '积极概率','支持','反对','ip属地']
    # csv_window = LoadCsvWindow(newfilepath)  # 创建第二个窗口实例
    # csv_window.load_csv(column_names)
    # csv_window.show()  # 显示第二个窗口
    # app.exec_()
    csv_file = 'TiebaAnalysis/聊聊二次元遗老这个问题，非引战【bilibili吧】_百度贴吧.csv'
    visualize_sentiments(csv_file)
    # chart.render('./HTML/sentiments_map.html')
    print("successful")

