import time

import csv
import os
import pandas as pd
from predict import get_sentiment_label


def write_to_csv(csv_path, input_text, negative, positive):
    # 获取识别结果
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sentiment_label = get_sentiment_label(negative, positive)

    # 获取目录路径
    directory = os.path.dirname(csv_path)

    # 如果目录不存在，则创建目录
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 将数据写入CSV文件
    with open(csv_path, 'a', newline='', encoding='utf-8-sig') as csvfile:  # 注意这里使用了 utf-8-sig
        fieldnames = ['时间', '文本', '识别结果', '消极概率', '积极概率']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 如果是新文件，需要重新写入表头
        if csvfile.tell() == 0:
            writer.writeheader()

        # 写入数据行
        writer.writerow({'时间': current_time, '文本': input_text, '识别结果': sentiment_label, '消极概率': negative,
                         '积极概率': positive})
def write_to_csv_tieba(csv_path, input_text, negative, positive,agree, disagree, ip_address,gender):
    # 获取识别结果
    # current_time = time.strftime("%Y-%m-%d", time.localtime())
    sentiment_label = get_sentiment_label(negative, positive)
    # 获取目录路径
    directory = os.path.dirname(csv_path)
    # 如果目录不存在，则创建目录
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 将数据写入CSV文件
    with open(csv_path, 'a', newline='', encoding='utf-8-sig') as csvfile:  # 注意这里使用了 utf-8-sig
        fieldnames = ['文本', '识别结果', '消极概率', '积极概率', '支持','反对','IP地址','评论者性别']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 如果是新文件，需要重新写入表头
        if csvfile.tell() == 0:
            writer.writeheader()

        # 写入数据行
        writer.writerow({'文本': input_text, '识别结果': sentiment_label, '消极概率': negative,
                         '积极概率': positive, '支持':agree,'反对':disagree,'IP地址': ip_address,'评论者性别':gender})


def read_columns_from_csv(filename, column1, column2):
    data1 = []  # 存储第一列数据的列表
    data2 = []  # 存储第二列数据的列表
    with open(filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)  # 创建 CSV 字典阅读器
        for row in reader:
            value1 = row[column1]  # 获取第一列指定列名的数据
            value2 = row[column2]  # 获取第二列指定列名的数据
            data1.append(value1)  # 将第一列数据添加到列表中
            data2.append(value2)  # 将第二列数据添加到列表中
    return data1, data2
def read_5columns_from_csv(filename, column1, column2, column3, column4,column5):
    data1 = []  # 存储第一列数据的列表
    data2 = []  # 存储第二列数据的列表
    data3 = []  # 存储第三列数据的列表
    data4 = []  # 存储第四列数据的列表
    data5 = []  # 存储第五列数据的列表
    with open(filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)  # 创建 CSV 字典阅读器
        for row in reader:
            value1 = row[column1]  # 获取第一列指定列名的数据
            value2 = row[column2]  # 获取第二列指定列名的数据
            value3 = row[column3]  # 获取第三列指定列名的数据
            value4 = row[column4]  # 获取第四列指定列名的数据
            value5 = row[column5]  # 获取第五列指定列名的数据
            data1.append(value1)  # 将第一列数据添加到列表中
            data2.append(value2)  # 将第二列数据添加到列表中
            data3.append(value3)  # 将第三列数据添加到列表中
            data4.append(value4)  # 将第四列数据添加到列表中
            data5.append(value5)  # 将第五列数据添加到列表中
    return data1, data2,data3,data4,data5