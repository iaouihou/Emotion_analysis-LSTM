import csv

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

# 示例用法
filename = './TieBaData/【图片】牛爷爷们我这事做的对吗？【显卡吧】_百度贴吧_8943071320_posts.csv'
column1 = 'Text'
column2 = 'IP Address'
texts, ip_addresses = read_columns_from_csv(filename, column1, column2)
for text, ip_address in zip(texts, ip_addresses):
    print("Text:", text)
    print("IP Address:", ip_address)
    print()
