import re

def remove_square_brackets(input_file, output_file):
    with open(input_file, 'r', encoding='gbk') as infile:
        with open(output_file, 'w', encoding='gbk') as outfile:
            for line in infile:
                # 使用正则表达式匹配方括号及其中的内容，并将其删除
                cleaned_line = re.sub(r'\[.*?\]', '', line)
                outfile.write(cleaned_line)

if __name__ == "__main__":
    input_file = 'data.txt'  # 输入文本文件名
    output_file = 'remove[].txt'  # 输出文本文件名
    remove_square_brackets(input_file, output_file)
