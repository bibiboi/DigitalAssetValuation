from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import time

print('over')
# input = pd.read_csv('final_shuju3.csv', encoding='GBK', header=None)
begin_time = time.time()
input = pd.read_csv('final_data.csv', encoding='GBK', header=None)
input = input.dropna(axis=0, how='any')
input = input.reset_index(drop=True)

output = input.loc[:, 6]
output = output.to_frame()
input = input.loc[:, 1:5]

clf = MLPRegressor(solver='adam', alpha=0.0, hidden_layer_sizes=(64,32,16,4),
                   random_state=1, activation='relu', max_iter=10000, batch_size=512)

# clf = MLPRegressor(solver='adam', alpha=0, hidden_layer_sizes=(32,16,4),
#                    random_state=1, activation='relu', max_iter=10000, batch_size=256)


x_train, x_test, y_train, y_test = train_test_split(input, output, test_size=0.3, random_state=0)

x_train = x_train.values
x_test = x_test.values
y_train = y_train.values
y_test = y_test.values
y_train = y_train.astype(np.float)
y_test = y_test.astype(np.float)

# 标准化
scaler = StandardScaler()  # 标准化转换
scaler.fit(x_train)  # 训练标准化对象
x_train = scaler.transform(x_train)  # 转换训练集
x_test = scaler.transform(x_test)   # 转换测试集
joblib.dump(scaler,'scaler.joblib')
# 归一化
# min_max_scaler = preprocessing.MinMaxScaler()
# min_max_scaler.fit(x_train)
# x_train = min_max_scaler.transform(x_train)
# x_test = min_max_scaler.transform(x_test)

clf.fit(x_train, y_train.ravel())
end_time = time.time()
print('训练集预测结果：', clf.score(x_train, y_train.ravel()))
score = clf.score(x_test, y_test.ravel())
print('测试集预测结果：', clf.score(x_test, y_test.ravel()))  # 预测结果
y_predict = clf.predict(x_test)
y = clf.predict(x_train)
np.set_printoptions(suppress=True)  # 输出数字不以科学计数法保存

print('计算效率：', end_time - begin_time)  # 预测结果

xx=range(0,len(y_train))
plt.figure(figsize=(8,6))
plt.scatter(xx,y_train,color="red",label="Sample Point",linewidth=3)
plt.plot(xx,y,color="orange",label="Fitting Line",linewidth=2)
plt.legend()
plt.show()
# 
joblib.dump(clf,'mlp.m')


# print(y_predict)
# print(y_test)