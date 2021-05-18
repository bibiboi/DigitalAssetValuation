import os
import math
from datetime import datetime

from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename

from forms import testform, uploadform, fielupload
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)
app.config['WTF_CSRF_SECRET_KEY']='abcd'
app.config['UPLOAD_PATH'] = os.path.join(os.path.dirname(__file__),'UserData')
app.secret_key = 'any'

data_name = ['无数据估值']
data_price = [0]


@app.route('/',methods=('GET', 'POST'))
def index():
    fielform = uploadform()#表单元素上传的form
    fielupform = fielupload()#文件上传的form
    img = [
        '/static/images/流星1.png',
        '/static/images/名称.png',
        '/static/images/类型.png',
        '/static/images/标签.png',
        '/static/images/海关数据.png',
        '/static/images/数据格式.png',
        '/static/images/时间.png',
        '/static/images/数量.png'
    ]
    #wtf处理文件
    if request.method == 'POST':
        if fielupform.validate_on_submit():
            f = fielupform.fiel.data
            filename = secure_filename(f.filename)#把上传的文件的名字改为安全的格式
            file_name = os.path.join(app.config['UPLOAD_PATH'], filename)#选择文件保存的地址，保存的名字
            f.save(file_name)#保存
            df = pd.read_excel(file_name)
            df['价格'] = 0
            y = predict(df)  # 预测所得结果

            print('上传成功')
            return redirect('/processed/1')
        elif fielform.validate_on_submit():
            data = [
                fielform.dataN.data,
                fielform.dataT.data,
                fielform.dataL.data,
                fielform.dataA.data,
                # fielform.dataF.data,
                request.form.get('startTime'),#str类型 2020-04-08 2022-04-04
                request.form.get('endTime'),
                fielform.dataS.data,
                fielform.dataSC.data
            ]
            # print(data[5])

            # 预测模型
            dataLabel = judgeLabels(data[2])
            dataInd = ['数据名称', '店铺', '数据标签', '数据大小', '浏览量', '价格']
            final_data = [[data[0], data[6], dataLabel, data[3], data[7], 0]]
            df = pd.DataFrame(final_data, columns=dataInd)
            print(df)
            y = predict(df)  # 预测所得结果

            # if data[4]=="" or data[5]=="":
            #     flash('时间不合法', 'error')
            # else:
            #     timeS = datetime.strptime(data[4], '%Y-%m-%d')
            #     timeE = datetime.strptime(data[5], '%Y-%m-%d')
            #     if timeS>timeE or timeE>datetime.now():
            #         flash('时间不合法', 'error')
            #     else:
            return redirect('/processed/1')

        else:
            print(fielform.errors)
            print(fielupform.errors)
            return render_template('index.html', img=img, fielform=fielform, fielupform=fielupform)

    return render_template('index.html', img=img, fielform=fielform, fielupform=fielupform)

# class page():
#     # has_pre = True
#     # has_next = True
#     page_num = 0
#     items = []
#     def __init__(self,datas):#该页数据
#         self.items.append(datas)#一个二维列表，每个元素为对应页数据的列表

def judgeLabels(label):
    if label == '2':
        return '智能投资'
    elif label == '4':
        return '智能风控'
    elif label == '5':
        return '智能客服'
    elif label == '6':
        return '智能识别'
    elif label == '7':
        return '手机号验证'
    elif label == '8':
        return '车辆信息 智能识别'
    elif label == '9':
        return '电子商务 商品信息'

def predict(Data):
    data = Data.copy()
    for i, v in data['数据大小'].items():
        # length = len(data['数据大小'][i])
        data['数据大小'].loc[i] = float(data['数据大小'].loc[i]) * 1024 * 1024

    data = data.dropna(subset=['数据标签'])
    data = data.dropna(subset=['数据名称'])
    data = data.dropna(subset=['店铺'])
    pages_name = data['数据名称'].values.tolist()

    # enc = TargetEncoder(cols=['数据名称', '店铺', '数据标签'])
    # enc.fit(data, data['价格'])
    # from mlp import encoding
    # data1 = encoding.enc.transform(data)

    dataframe = pd.DataFrame({'数据名称': data['数据名称'], '店铺': data['店铺'],
                              '数据标签': data['数据标签'], '数据大小': data['数据大小'],
                              '浏览量': data['浏览量'], '价格': data['价格']})
    enc = joblib.load('encoding.joblib')
    dataframe = enc.transform(dataframe)

    dataframe.drop(columns='价格', inplace=True)
    scaler = joblib.load('scaler.joblib')
    dataframe = scaler.transform(dataframe)
    clf = joblib.load('mlp.m')
    print(dataframe)
    # print(dataframe.iloc[:,:-1])
    # data = dataframe.values
    # data = data.astype(np.float)
    # data = MLP.scaler.transform(data)

    pages_price = list(clf.predict(dataframe)/10)
    # print("名称：", pages_name, type(pages_name), "size", len(pages_name))
    data_pages.insert(pages_name,pages_price)
    # print("名称：",data_pages.pages_name ,type(data_pages.pages_name), "size", len(data_pages.pages_name))
    np.set_printoptions(suppress=True)  # 输出数字不以科学计数法保存


    return data_price

#

class Pages():
    pages_name = []#各页数据名称数据
    pages_price = []
    pages_num = 0
    pages_size = 0
    def __init__(self,size):#分页大小和数据列表
        self.pages_size = size
            # if i != self.pages_num-1:
            #     self.pages_name.append(name[i*size:(i+1)*size])
            #     self.pages_price.append(price[i*size:(i+1)*size])
            # else:
            #     self.pages_name.append(name[i*size:len(name)+1])
            #     self.pages_price.append(price[i*size:len(name)+1])
    def insert(self,name,price):
        print(len(name))
        self.pages_num = math.ceil(len(name) / self.pages_size)  # 页数从1开始
        for i in range(self.pages_num):  # 右开
            self.pages_name.append(name[i * self.pages_size:min((i + 1) * self.pages_size, len(name) + 1)])
            self.pages_price.append(price[i * self.pages_size:min((i + 1) * self.pages_size, len(price) + 1)])
        print('class', self.pages_name, type(self.pages_name), len(self.pages_name))


# data_pages = Pages(2,data_name,data_price)#创建Pages对象
data_pages = Pages(10)#创建Pages对象

@app.route('/processed/<int:page>',methods=('GET', 'POST'))
def result(page):#当前页面
    if request.method == 'GET':
        bg = '/static/images/bg.jpg'
        # print("size:",len(data_pages.pages_name), len(data_pages.pages_price))

        page_name = data_pages.pages_name[page-1]#当前页面的数据
        page_price = data_pages.pages_price[page-1]
        nums = data_pages.pages_num
        print(page)
        print(page_name,'size',type(page_name),len(page_name))
        print(page_price)
        return render_template('processed.html',page_name=page_name,page_price=page_price,page=page,nums=nums,bg=bg)
    if request.method == 'POST':
        return redirect('/')

@app.route('/test',methods=('GET', 'POST'))
def test():
    form = testform()
    if form.validate_on_submit():
        print(form.select.data)
    return render_template('test.html', form=form)

if __name__ == '__main__':
   app.run()