from mycsv.csv import write_to_csv
from predict import predict_sentiment, get_sentiment_label
import csv


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
def Analysis(csv_path,column_name):
    column_data = read_csv_column(csv_path, column_name)
    if column_data:
        for input_text in column_data:
            negative, positive = predict_sentiment(input_text, pad_size=50)
            new_csv_path = "results/" + csv_path
            # print(new_csv_path)
            write_to_csv(new_csv_path, input_text, negative, positive)
    else:
        print("Failed to read column data.")
    return new_csv_path

csv_path = "TieBaData/【图片】我的逆天沸羊羊舍友给女朋友下跪求原谅【孙笑川吧】_百度贴吧_8930857397_posts.csv"
column_name = "\ufeffText"
print(Analysis(csv_path,column_name))
