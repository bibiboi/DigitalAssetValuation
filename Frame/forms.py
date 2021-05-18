from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SelectField, SubmitField, FileField, SelectMultipleField, DateField, BooleanField
from wtforms.validators import DataRequired, ValidationError


class uploadform(FlaskForm):
    dataN = StringField(label='数据名称', render_kw={
        'class': 'form-control',
        'id': 'exampleInputEmail1',
        # 'required': False
    },
                        # validators=[DataRequired('请输入数据名称！')]
                        )
    dataT = SelectField(label='数据类型', render_kw={
        'class': 'form-control',
        'id': 'exampleInputEmail1',
    },
                        choices=[(2, '图片'), (3, '文本')]
                        )
    dataL = SelectField(label='数据标签', render_kw={
        'class': 'form-control',
        'id': 'exampleInputEmail1',

    },
                        choices=[(2, '智能投资'), (4, '智能风控'),
                                 (5, '智能客服'), (6, '智能识别'), (7, '手机号验证'), (8, '车辆信息 智能识别'),
                                 (9, '电子商务 商品信息')
                                 ]
                        )
    dataA = StringField(label='数据大小', render_kw={
        'class': 'form-control',
        'id': 'exampleInputEmail1',
        'required': False
    },
                        validators=[DataRequired('请输入数据大小')]
                        )
    # dataF = SelectField(label='数据格式', render_kw={
    #     'class': 'form-control',
    #     'id': 'exampleInputEmail1'
    # },
    #     choices=[(1, 'null'), (2, 'pdf'), (3,'excel'), (4, '.xlsx'),
    #              (5, 'jpg jpeg png等')
    #              ]
    # )

    dataS = StringField(label='数据店铺', render_kw={
        'class': 'form-control',
        'id': 'exampleInputEmail1',
        'required': False
    })

    dataSC = StringField(label='数据浏览量', render_kw={
        'class': 'form-control',
        'id': 'exampleInputEmail1',
        'required': False
    })



    def validate_dataN(self, dataN):
        if dataN.data == "":
            raise ValidationError('请输入数据名称！')
        return dataN

    def validate_dataL(self, dataL):
        if dataL.data == "":
            raise ValidationError('请输入数据标签！')
        return dataL

    def validate_dataA(self, dataA):
        if dataA.data == "":
            raise ValidationError('请输入数据大小！')
        return dataA

    def validate_dataS(self, dataS):
        if dataS.data == "":
            raise ValidationError('请输入数据规格！')
        return dataS

    def validate_dataSC(self, dataSC):
        if dataSC.data == "":
            raise ValidationError('请输入数据浏览量！')
        return dataSC

class fielupload(FlaskForm):
    fiel = FileField(label='上传', validators=[
        FileRequired('请选择文件'),
        FileAllowed(['xlsx'], '仅支持xlsx')  # 前项是列表，后项是错误提示
    ],
            render_kw={
                         'required': False
            }
    )

class testform(FlaskForm):
    select = SelectField(
        label='类别',
        validators=[DataRequired('请选择标签')],
        render_kw={
            'class': 'form-control'
        },
        choices=[(1, '情感'), (2, '星座'), (3, '爱情')],
        default = 3,
        coerce=int
    )

    submit = SubmitField('上传')