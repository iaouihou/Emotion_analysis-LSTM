import time

import csv
import os

from predict import get_sentiment_label
def write_to_csv(csv_path, input_text, negative, positive):
    # 获取识别结果
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sentiment_label = get_sentiment_label(negative, positive)
    # 检查CSV文件是否存在，如果不存在，则创建一个新文件并写入表头
    is_new_file = False
    if not os.path.exists(csv_path):
        is_new_file = True

    # 将数据写入CSV文件
    with open(csv_path, 'a', newline='', encoding='utf-8-sig') as csvfile:  # 注意这里使用了 utf-8-sig
        fieldnames = ['时间', '文本', '识别结果', '消极概率', '积极概率']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 如果是新文件，需要重新写入表头
        if is_new_file:
            writer.writeheader()

        # 写入数据行
        writer.writerow({'时间': current_time, '文本': input_text, '识别结果': sentiment_label,'消极概率': negative,
                         '积极概率': positive})

def read_csv_column(filename, column_name):
    texts = []
    with open(filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)  # 创建 CSV 字典阅读器
        for row in reader:
            texts.append(row[column_name])
    return texts