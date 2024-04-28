# -*- coding: utf-8 -*-
import numpy as np
import pickle as pkl
from datetime import timedelta
import torch.nn as nn
import time
import torch
from collections import OrderedDict
import torch.nn.functional as F

# 超参数设置
vocab_path = './data/vocab.pkl'  # 词表
stop_words_path = './data/stopwords.txt'  # 停用词文件路径
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
pad_size = 50  # 每句话处理成的长度(短填长切)
hidden_size = 128  # lstm隐藏层
num_layers = 2  # lstm层数
MAX_VOCAB_SIZE = 10000  # 词表长度限制
UNK, PAD = '<UNK>', '<PAD>'  # 未知字，padding符号



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
    words_line = []
    tokenizer = lambda x: [y for y in x]  # 字级别分词
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


def predict_sentiment(text, pad_size):
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
        return round(negative, 2), round(active, 2)
def get_sentiment_label(negative, positive):
    # 如果negative和positive之差小于0.2，则认为是中性
    if abs(negative - positive) < 0.31:
        return "中性"
    # 否则，根据negative和positive的比例来确定情感
    elif negative > positive:
        return "消极"
    elif negative < positive:
        return "积极"
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


np.random.seed(1)
torch.manual_seed(1)
torch.cuda.manual_seed_all(1)
torch.backends.cudnn.deterministic = True

start_time = time.time()
print("Loading data...")
vocab = pkl.load(open(vocab_path, 'rb'))
time_dif = get_time_dif(start_time)
print("Time usage:", time_dif)

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model = Model().to(device)

    # 加载模型
model = Model()

# 加载训练好的模型参数
model_path = './saved_dict/lstm_waimai.ckpt'
model = load_model(model, model_path)

if __name__ == '__main__':
    # 进行情感预测
    print(predict_sentiment("在这放一只猫猫，看书看累的人可以摸摸它，路过的人可以摸摸她，但是别摸死了／l、（ﾟ､ 。 ７l、 ~ヽじしf_, )ノ 祝摸过的人好运连连，身体健康，开开心心哦",pad_size=50))