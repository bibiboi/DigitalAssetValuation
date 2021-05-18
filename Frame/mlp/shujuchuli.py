import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder


np.set_printoptions(linewidth=10000)
data = pd.read_csv('/Users/taoshuai/Desktop/研究生学习资料/外包大赛/京东万象数据删除450000.csv',encoding='GBK')
# csv_reader=csv.reader(open('/Users/taoshuai/Desktop/研究生学习资料/外包大赛/京东万象数据.csv',encoding='GBK'))


pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)




def One_hot(data):
    np.set_printoptions(threshold=1e6) # 输出时保证将所有元素输出
    le_sex=LabelEncoder().fit(data)
    Sex_label=le_sex.transform(data)
    Sex_label= LabelEncoder().fit_transform(data) #fit_transform等价于fit和transform两个函数结合
    ohe_sex=OneHotEncoder(sparse=False).fit(Sex_label.reshape(-1,1))
    Sex_ohe=ohe_sex.transform(Sex_label.reshape(-1,1))
    Sex_ohe_3 = OneHotEncoder(sparse=False).fit_transform(Sex_label.reshape((-1,1)))

    return Sex_ohe_3




def fill_miss_byRandomForest(data_df , obj_column, missing_other_column):
    # 先把有缺失的其他列删除掉missing_other_column
    data_df = data_df.drop(missing_other_column , axis = 1)
    data_df = data_df.dropna(subset=['价格'])
    print(type(data_df[obj_column][0]))

    # 分成已知该特征和未知该特征两部分
    known = data_df[data_df[obj_column].notnull()]
    for i, v in known[obj_column].items():
        length = len(known[obj_column][i])
        print(length)
        if(known[obj_column][i][length-2] == 'K'):
            known.loc[:, (obj_column)][i] = float(known[obj_column][i][0:length - 2]) * 1024
        else:
            known.loc[:, (obj_column)][i] = float(known[obj_column][i][0:length - 2]) * 1024 * 1024

    unknown = data_df[data_df[obj_column].isnull()]
    # y为结果标签值
    y_know = known[obj_column]
    # X为特征属性值
    X_know= known.drop(obj_column , axis = 1)
    from sklearn.ensemble import RandomForestRegressor
    rfr = RandomForestRegressor(random_state=0, n_estimators=200,max_depth=3,n_jobs=-1)
    rfr.fit(X_know['价格'].to_frame(),y_know)
    # 用得到的模型进行未知特征值预测
    # X为特征属性值
    X_unknow= unknown.drop(obj_column , axis = 1)
    predicted = rfr.predict(X_unknow['价格'].to_frame()).round(0)
    data_df.loc[(data_df[obj_column].isnull()), obj_column] = predicted
    return data_df


data.describe()
data.columns.tolist()
### 调用fill_miss_byRandomForest函数，补充MonthlyIncome的缺失值
data1_MonthlyIncome=fill_miss_byRandomForest(data, '数据大小', '交易量')
data1_MonthlyIncome.to_csv('/Users/taoshuai/Desktop/研究生学习资料/外包大赛/京东万象数据填充3.csv',encoding='GBK')
