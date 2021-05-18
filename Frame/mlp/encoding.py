import pandas as pd
from category_encoders import TargetEncoder
import joblib

data = pd.read_csv('./京东万象数据填充2.csv', encoding='GBK')
data = data.dropna(subset=['价格'])
data = data.dropna(subset=['数据标签'])
data = data.dropna(subset=['数据名称'])
data = data.dropna(subset=['店铺'])

enc = TargetEncoder(cols=['数据名称', '店铺', '数据标签'])
# print(type(enc))
dataframe = data[['数据名称','店铺','数据标签','数据大小','浏览量','价格']]
enc.fit(dataframe, dataframe['价格'])

data1 = enc.transform(dataframe)
# print(type(data1))
# dataframe = pd.DataFrame({'数据名称': data1['数据名称'], '店铺': data1['店铺'],
#                           '数据标签': data1['数据标签'], '数据大小': data1['数据大小'],
#                           '浏览量': data1['浏览量'], '价格': data1['价格']})
joblib.dump(enc,'encoding.joblib')
data1.to_csv('final_data.csv', encoding='GBK', sep=',')
