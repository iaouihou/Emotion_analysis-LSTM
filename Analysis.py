from PyQt5.QtWidgets import QApplication

from LoadCsv import LoadCsvWindow
from mycsv.csv import write_to_csv
from predict import predict_sentiment, get_sentiment_label
import csv
from mycsv.csv import *


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
def Analysis_tieba(csv_path, filename, column1_name, column2_name):
    # column_data = read_csv_column(csv_path, column_name)
    column1_data, column2_data = read_columns_from_csv(csv_path, column1_name, column2_name)
    if column1_data and column2_data:
        for input_text, ip in zip(column1_data, column2_data):
            print(input_text+ip)
            negative, positive = predict_sentiment(input_text, pad_size=50)
            new_csv_path =f'TiebaAnalysis/{filename}.csv'
            # print(new_csv_path)
            write_to_csv_ip(new_csv_path, input_text, negative, positive,ip)
    else:
        print("Failed to read column data.")
    return new_csv_path

if __name__ == "__main__":
    csv_path = "TieBaData/逆天室友求求你别恶心我了【新孙笑川吧】_百度贴吧_8938247271_posts.csv"
    filename = "逆天室友求求你别恶心我了【新孙笑川吧】_百度贴吧_8938247271_posts"
    column1_name = "Text"
    column2_name = "IP Address"
    newfilepath = Analysis_tieba(csv_path, filename, column1_name, column2_name)
    print(newfilepath)
    app = QApplication([])
    column_names = ['时间', '文本', '识别结果', '消极概率', '积极概率','ip属地']
    csv_window = LoadCsvWindow(newfilepath)  # 创建第二个窗口实例
    csv_window.load_csv(column_names)
    csv_window.show()  # 显示第二个窗口
    app.exec_()
