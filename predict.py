# -*- coding: utf-8 -*-
import numpy as np
import pickle as pkl
from tqdm import tqdm
from datetime import timedelta
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import time
import torch
from sklearn.model_selection import train_test_split
from collections import OrderedDict
import torch.nn.functional as F
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QTextEdit, QPushButton, QVBoxLayout, QWidget, \
    QLabel, QDialog

# 超参数设置
data_path = './data/data.txt'  # 数据集
vocab_path = './data/vocab.pkl'  # 词表
save_path = './saved_dict/lstm.ckpt'  # 模型训练结果
embedding_pretrained = \
    torch.tensor(
        np.load(
            './data/embedding_Tencent.npz')
        ["embeddings"].astype('float32'))
# 预训练词向量
embed = embedding_pretrained.size(1)  # 词向量维度
dropout = 0.5  # 随机丢弃
num_classes = 2  # 类别数
num_epochs = 30  # epoch数
batch_size = 128  # mini-batch大小
pad_size = 50  # 每句话处理成的长度(短填长切)
learning_rate = 1e-3  # 学习率
hidden_size = 128  # lstm隐藏层
num_layers = 2  # lstm层数
MAX_VOCAB_SIZE = 10000  # 词表长度限制
UNK, PAD = '<UNK>', '<PAD>'  # 未知字，padding符号


def get_data():
    tokenizer = lambda x: [y for y in x]  # 字级别
    vocab = pkl.load(open(vocab_path, 'rb'))
    print('vocab', vocab)
    print(f"Vocab size: {len(vocab)}")

    train, dev, test = load_dataset(data_path, pad_size, tokenizer, vocab)
    return vocab, train, dev, test


def load_dataset(path, pad_size, tokenizer, vocab):
    contents = []
    n = 0
    with open(path, 'r', encoding='gbk') as f:
        for line in tqdm(f):
            lin = line.strip()
            if not lin:
                continue
            label, content = lin.split('	####	')
            words_line = []
            token = tokenizer(content)
            seq_len = len(token)
            if pad_size:
                if len(token) < pad_size:
                    token.extend([vocab.get(PAD)] * (pad_size - len(token)))
                else:
                    token = token[:pad_size]
                    seq_len = pad_size
            for word in token:
                words_line.append(vocab.get(word, vocab.get(UNK)))
            n += 1
            contents.append((words_line, int(label)))

    train, X_t = train_test_split(contents, test_size=0.4, random_state=42)
    dev, test = train_test_split(X_t, test_size=0.5, random_state=42)
    return train, dev, test


class TextDataset(Dataset):
    def __init__(self, data):
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.x = torch.LongTensor([x[0] for x in data]).to(self.device)
        self.y = torch.LongTensor([x[1] for x in data]).to(self.device)

    def __getitem__(self, index):
        self.text = self.x[index]
        self.label = self.y[index]
        return self.text, self.label

    def __len__(self):
        return len(self.x)


def get_time_dif(start_time):
    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        # 使用预训练的词向量模型，freeze=False 表示允许参数在训练中更新
        # 在NLP任务中，当我们搭建网络时，第一层往往是嵌入层，对于嵌入层有两种方式初始化embedding向量，
        # 一种是直接随机初始化，另一种是使用预训练好的词向量初始化。
        self.embedding = nn.Embedding.from_pretrained(embedding_pretrained, freeze=False)
        # bidirectional=True表示使用的是双向LSTM
        self.lstm = nn.LSTM(embed, hidden_size, num_layers,
                            bidirectional=True, batch_first=True, dropout=dropout)
        # 因为是双向LSTM，所以层数为config.hidden_size * 2
        self.fc = nn.Linear(hidden_size * 2, num_classes)
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')  # 添加device属性

    def forward(self, x):
        out = self.embedding(x)
        # lstm 的input为[batchsize, max_length, embedding_size]，输出表示为 output,(h_n,c_n),
        # 保存了每个时间步的输出，如果想要获取最后一个时间步的输出，则可以这么获取：output_last = output[:,-1,:]
        out, _ = self.lstm(out)
        out = self.fc(out[:, -1, :])  # 句子最后时刻的 hidden state
        return out


def preprocess(text, vocab, pad_size):
    tokenizer = lambda x: [y for y in x]  # 字级别分词
    words_line = []
    token = tokenizer(text)
    seq_len = len(token)
    if pad_size:
        if len(token) < pad_size:
            token.extend([vocab.get(PAD)] * (pad_size - len(token)))
        else:
            token = token[:pad_size]
            seq_len = pad_size
    for word in token:
        words_line.append(vocab.get(word, vocab.get(UNK)))
    return torch.tensor(words_line).unsqueeze(0)


def predict_sentiment(text, model, vocab, pad_size):
    # 将模型设置为评估模式
    model.eval()
    with torch.no_grad():
        input_tensor = preprocess(text, vocab, pad_size)
        # 将输入张量移动到模型所在的设备上
        # input_tensor = input_tensor.to(model.device)
        outputs = model(input_tensor)
        _, predicted = torch.max(outputs.data, 1)
        probabilities = F.softmax(outputs, dim=1)
        negative=probabilities.cpu().numpy()[0][0]
        active=probabilities.cpu().numpy()[0][1]
        results="消极的概率:"+str(negative)+"\n积极的概率:"+str(active)
        return results

def load_model(model, model_path):
    # 加载模型参数
    state_dict = torch.load(model_path)
    # 如果state_dict是由GPU保存并且在CPU上加载的，则需要将所有参数的名称中的‘.cuda：n’删除
    if list(state_dict.keys())[0].startswith("module."):
        new_state_dict = OrderedDict()
        for k, v in state_dict.items():
            name = k[7:]  # 去除'module.'前缀
            new_state_dict[name] = v
        # 加载参数
        model.load_state_dict(new_state_dict)
    else:
        model.load_state_dict(state_dict)
    return model

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('情感分析系统')
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.create_menu_bar()
        self.create_widgets()

    def create_menu_bar(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu('Help')
        about_action = QAction('About...', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def create_widgets(self):
        self.input_text_edit = QTextEdit()
        self.layout.addWidget(self.input_text_edit)

        self.analysis_result_label = QLabel('分析结果：')
        self.analysis_result_label.setStyleSheet("font: 15pt Helvetica;")
        self.layout.addWidget(self.analysis_result_label)

        self.output_news_label = QLabel()
        self.output_news_label.setStyleSheet("font: 15pt Helvetica;")
        self.layout.addWidget(self.output_news_label)

        self.start_button = QPushButton('开始')
        self.start_button.setStyleSheet("font: 15pt Helvetica;")
        self.start_button.clicked.connect(self.analyze_sentiment)
        self.layout.addWidget(self.start_button)

        self.clear_button = QPushButton('清空')
        self.clear_button.setStyleSheet("font: 15pt Helvetica;")
        self.clear_button.clicked.connect(self.clear_input)
        self.layout.addWidget(self.clear_button)

    def show_about_dialog(self):
        about_dialog = QDialog()
        about_dialog.setWindowTitle('About')
        about_layout = QVBoxLayout()
        about_label = QLabel('你好')
        about_layout.addWidget(about_label)
        about_dialog.setLayout(about_layout)
        about_dialog.exec()

    def analyze_sentiment(self):
        # input_text = self.input_text_edit.toPlainText()
        input_text = predict_sentiment(self.input_text_edit.toPlainText(), model, vocab, pad_size=50)
        # 这里需要调用情感分析函数，并将结果更新到输出标签中
        # 现在仅将输入文本设置为输出结果
        self.output_news_label.setText(input_text)

    def clear_input(self):
        self.input_text_edit.clear()
        self.output_news_label.clear()


np.random.seed(1)
torch.manual_seed(1)
torch.cuda.manual_seed_all(1)
torch.backends.cudnn.deterministic = True

start_time = time.time()
print("Loading data...")
vocab, train_data, dev_data, test_data = get_data()
time_dif = get_time_dif(start_time)
print("Time usage:", time_dif)

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model = Model().to(device)

    # 加载模型
model = Model()

# 加载训练好的模型参数
model_path = './saved_dict/lstm.ckpt'
model = load_model(model, model_path)


if __name__ == '__main__':
    # 进行情感预测
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())