from flask import Flask,render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,FileField,TextAreaField
from wtforms.validators import DataRequired,Length
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    id=StringField('用户名:',validators=[DataRequired()])
    password=PasswordField('密码:',validators=[DataRequired()])
    submit=SubmitField('登录')
class RegisterForm(FlaskForm):
    id = StringField('新的用户名:',validators=[DataRequired()])
    password = PasswordField('密码:', validators=[DataRequired()])
    submit = SubmitField('注册')
class EditProfileForm(FlaskForm):
    name=StringField('姓名:')
    sex=StringField('性别:')
    location=StringField('地址:')
    about_me=StringField('个人简介:')
    submit=SubmitField('保存')
class Modifypassword_Form(FlaskForm):
    old_password=StringField('旧密码:',validators=[DataRequired()])
    new_password=StringField('新密码:',validators=[DataRequired()])
    submit=SubmitField('修改')
class Comment_Form(FlaskForm):
    comment=StringField('',validators=[DataRequired()])
    submit=SubmitField('发表评论')