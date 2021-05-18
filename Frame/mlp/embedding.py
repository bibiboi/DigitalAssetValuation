import gensim
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import logging
import pandas as pd

def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'a', encoding='GBK')
    print(len(data))
    for i in range(len(data)):
        s = str(data[i]).replace(" ", "")#去除空格
        s = s + ' '  # 每个字符末尾追加空格符
        file.write(s)
    file.close()
    print("保存文件成功")


def word2vec(data_txt):
    shuju = open(data_txt, 'r', encoding='GBK')
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model = Word2Vec(LineSentence(shuju), sg=1, size=100, window=10, min_count=1, workers=15, sample=1e-3)
    for key in model.wv.vocab:
        print(key)
        print(model.wv.vocab[key])
    print(len(model.wv.vocab))
    model.save('/Users/taoshuai/Desktop/研究生学习资料/外包大赛/text1.word2vec')
    vec = model.wv['人工智能行业周报12.4--12.10中科点击（北京）科技有限公司']
    print(vec)

# data = pd.read_csv('/Users/taoshuai/Desktop/研究生学习资料/外包大赛/京东万象数据填充.csv', encoding='GBK')
# print(data.head())
# data['1'] = data['数据名称'].map(str) + data['店铺'].map(str)
# data['1'] = data['1'].astype(str)
# data['1'] = data['1'].apply(lambda x : x.replace(' ', ''))
# print(data['1'])
# data['2'] = data['价格'].map(str)
# data['3'] = data['浏览量'].map(str)
# data['4'] = data['数据大小'].map(str)
# dataframe = pd.DataFrame({'数据名称': data['1'], '价格': data['2'], '浏览量': data['3'], '数据大小': data['4']})
# dataframe.to_csv('/Users/taoshuai/Desktop/研究生学习资料/外包大赛/京东万象数据6.csv', encoding='GBK', sep=',')

# text_save('text1.txt', data['new'])
# word2vec('text1.txt')
# frame = pd.read_csv('/Users/taoshuai/Desktop/研究生学习资料/外包大赛/京东万象数据6.csv', encoding='GBK')
# data = frame.drop_duplicates(subset=['数据名称'], keep='first', inplace=False)
# data.to_csv('/Users/taoshuai/Desktop/研究生学习资料/外包大赛/京东万象数据7.csv', encoding='GBK')
# data = pd.read_csv('/Users/taoshuai/Desktop/研究生学习资料/外包大赛/京东万象数据7.csv', encoding='GBK')
# #
# #
# text_save('text_final3.txt', data['数据名称'])
#
# word2vec('text_final3.txt')



# model = Word2Vec.load('/Users/taoshuai/Desktop/研究生学习资料/外包大赛/text1.word2vec')
# for key in model.wv.vocab:
#     print(key)
#     print(model.wv.vocab[key])
# print(len(model.wv.vocab))
# vec = model.wv['熬最深的夜买最贵的装备”BJdata']
# print(vec)
# sim_words = model.wv.most_similar(positive=['身份证识别翔云人工智能开放平台'],topn=10)
# for word, similarity in sim_words:
#     print(word, similarity)

# data1 = pd.read_csv('/Users/taoshuai/Desktop/研究生学习资料/外包大赛/京东万象数据7.csv', encoding='GBK')
# text_save('text_final4.txt', data['数据名称'])
# text_save('text_final4.txt', data['店铺'])
# text_save('text_final4.txt', data1['数据名称'])
# word2vec('text_final4.txt')
# model = Word2Vec.load('/Users/taoshuai/Desktop/研究生学习资料/外包大赛/text1.word2vec')
#
#
# for i, v in data1['数据名称'].items():
#     vec = model.wv[v]
#     data1['数据名称'].loc[i] = vec
#
# data1.to_csv('/Users/taoshuai/Desktop/研究生学习资料/外包大赛/京东万象数据11.csv', encoding='GBK')


data = pd.read_csv('京东万象数据填充.csv', encoding='GBK')
for i, v in data['数据大小'].items():
    length = len(data['数据大小'][i])
    if (data["数据大小"][i][length - 2] == 'K'):
        data['数据大小'].loc[i] = float(data['数据大小'].loc[i][0:length - 2]) * 1024
    elif data["数据大小"][i][length - 2] == 'M':
        data['数据大小'].loc[i] = float(data['数据大小'].loc[i][0:length - 2]) * 1024 * 1024
    elif data["数据大小"][i][length - 2] == 'G':
        data['数据大小'].loc[i] = float(data['数据大小'].loc[i][0:length - 2]) * 1024 * 1024 * 1024
    else:
        pass

data.to_csv('京东万象数据填充2.csv', encoding='GBK')