def merge_txt_files(file1, file2, output_file):
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='gbk') as f2:
        data1 = f1.read()
        data2 = f2.read()

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(data1)
        outfile.write(data2)


# 合并两个txt文件为一个新文件
file1 = 'waimai_data.txt'
file2 = 'data.txt'
output_file = 'merged_data.txt'
merge_txt_files(file1, file2, output_file)
