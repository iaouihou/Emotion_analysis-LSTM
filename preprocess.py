import jieba
stop_words_path = './data/stopwords.txt'  # 停用词文件路径

def load_stop_words(stop_words_path):
    stop_words = []
    with open(stop_words_path, 'r', encoding='utf-8') as f:
        for line in f:
            stop_words.append(line.strip())
    return stop_words
def remove_stopwords(text, stopwords):
    # 使用jieba进行中文分词
    words = jieba.lcut(text)
    # 去除停用词
    filtered_words = [word for word in words if word not in stopwords]
    # 将过滤后的单词列表连接成字符串，保持原有格式
    print(filtered_words)
    processed_text = ' '.join(filtered_words)
    print()
    return processed_text