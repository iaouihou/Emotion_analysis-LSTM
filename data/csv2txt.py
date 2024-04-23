import csv

def csv_to_txt(csv_file, txt_file):
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        with open(txt_file, 'w', encoding='utf-8') as txt_file:
            for row in csv_reader:
                txt_file.write('\t####\t'.join(row) + '\n')  # 使用\t####\t分隔数据并写入文本文件

if __name__ == "__main__":
    csv_file = 'hotel.csv'  # CSV文件名
    txt_file = 'hotel_data.txt'  # 要生成的文本文件名
    csv_to_txt(csv_file, txt_file)
