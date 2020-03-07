#管理员账户密码都为‘admin’
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from flask import Flask,render_template,flash,redirect,url_for,request,send_from_directory,Response
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm,RegisterForm,EditProfileForm,Modifypassword_Form,Comment_Form
import pymysql
pymysql.install_as_MySQLdb()
import os
from flask_redis import FlaskRedis
import uuid
import datetime
app = Flask(__name__)
mysqlpassword=input("请输入您的mysql密码:")
#mysqlpassword = ''
app.config["SQLALCHEMY_DATABASE_URI"]='mysql://root:'+mysqlpassword+'@localhost:3306/first_flask?charset=utf8'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]='False'
app.secret_key='ljlhhh'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = ''
login_manager.login_message_category = "info"
db=SQLAlchemy(app)
login_manager.init_app(app)
app.config["REDIS_URL"] = "redis://127.0.0.1:6379/0"
rd = FlaskRedis(app)
rd.flushall()
class User(UserMixin,db.Model):
    __tablename__="users"
    id = db.Column(db.String(64),primary_key=True,unique=True)
    password = db.Column(db.String(64))
    location = db.Column(db.String(64))
    name = db.Column(db.String(36))
    sex = db.Column(db.String(12))
    about_me = db.Column(db.String(128))
    icon = db.Column(db.String(128), default=None)
    count = db.Column(db.String(64))
    count2=db.Column(db.String(128))
    count3 = db.Column(db.String(128))
    def __repr__(self):
        return '<User %r>'%self.id
class Video(db.Model):
    __tablename__='my_video'
    id=db.Column(db.String(64),primary_key=True)
    username=db.Column(db.String(64))
    videoaddress=db.Column(db.String(128),default=None)
    type=db.Column(db.String(64))
    thumb_up=db.Column(db.String(64))
    thumb_all=db.Column(db.String(128))
    danmakucount=db.Column(db.String(128))
    def __repr__(self):
        return '<Video %r>'%self.id
class Thumb_up(db.Model):
    __tablename__='thumb_up'
    id=db.Column(db.String(64),primary_key=True)
    video=db.Column(db.String(64))
    username=db.Column(db.String(64))
    def __repr__(self):
        return '<Thumb_up %r>'%self.id
class Comment(db.Model):
    __tablename__='comments'
    username=db.Column(db.String(128))
    comment=db.Column(db.String(256))
    id=db.Column(db.String(64),primary_key=True)
    video=db.Column(db.String(128))
    def __repr__(self):
        return '<Comment %r>'%self.id
class Collection(db.Model):
    __tablename__='collection'
    id=db.Column(db.String(128),primary_key=True)
    username=db.Column(db.String(128))
    collections=db.Column(db.String(128))
    def __repr__(self):
        return '<Collection %r>'%self.id

db.drop_all()
db.create_all()

def query_video(user_id):
    video = Video.query.filter(Video.username == user_id).all()
    if video:
        return video
def query_user(user_id):
    user = User.query.filter(User.id == user_id).first()
    if user:
        return user
ALLOWED_EXTENSIONSicon = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONSvideo=set(['flv','webm','mp4','ogg','swf'])
def allowed_iconfile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONSicon

def allwoed_videofile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONSvideo
adminid='admin'
adminpassword='admin'
admincount=1
admincount2=1
admincount3=1
adminicon='/iconfile/d8b95b0f7a2acb298f7d25dbba90b4eb.jpg'
adminro = User(id=adminid,password=adminpassword,count=admincount,count2=admincount2,count3=admincount3,icon=adminicon,
               location='未知',sex='未知',about_me='无',name='未知')
db.session.add(adminro)
db.session.commit()
@login_manager.user_loader
def load_user(user_id):
    if query_user(user_id) is not None:
        curr_user = User()
        curr_user.id = user_id
        return curr_user

@app.route('/')
def re():
    if not current_user:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('home'))

@app.route('/login/', methods=['GET', 'POST'])#登录
def login():
    login_form = LoginForm()
    if request.method == 'POST':
        user_id = login_form.id.data
        user = query_user(user_id)
        print(user_id)
        if user is not None and login_form.password.data == user.password:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('用户名或密码错误!')
            return redirect(url_for('login'))
    return render_template('login.html',login_form=login_form)

@app.route('/register/',methods=['GET','POST'])#注册
def register():
    register_form=RegisterForm()
    if request.method == 'POST':
        id = register_form.id.data
        password = register_form.password.data
        count=1
        count2=1
        count3=1
        icon='/iconfile/d8b95b0f7a2acb298f7d25dbba90b4eb.jpg'
        try:
            ro = User(id=id,password=password,count=count,count2=count2,count3=count3,icon=icon,location='未知',
                      sex='未知',about_me='无',name='未知')
            db.session.add(ro)
            db.session.commit()
            flash('注册成功')
        except:
            flash('该用户名已被注册')
            return redirect(url_for('register',next=request.url))
        return redirect('/login/')
    return render_template('register.html', register_form=register_form)

@app.route('/logout/')#登出
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home/')#主页
@login_required
def home():
    return render_template('home.html',adminid=current_user.id)

@app.route('/my_center/')#个人中心
@login_required
def personal_data():
    user=query_user(current_user.id)
    return render_template('personal_data.html',user=user)

@app.route('/editprofile/',methods=['GET','POST'])#改资料
@login_required
def editprofile():
    edit_form=EditProfileForm()
    user = query_user(current_user.id)
    if request.method == 'POST':
        if(edit_form.name.data is not ''):
            user.name = edit_form.name.data
        if (edit_form.sex.data is not ''):
            user.sex=edit_form.sex.data
        if (edit_form.location.data is not ''):
            user.location = edit_form.location.data
        if (edit_form.about_me.data is not ''):
            user.about_me = edit_form.about_me.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('personal_data'))
    return render_template('editproflie.html', edit_form=edit_form,user=user)

@app.route('/modify/',methods=['GET','POST'])#改密码
@login_required
def modify():
    modify_form = Modifypassword_Form()
    if request.method == 'POST':
        user = query_user(current_user.id)
        if(user.password==modify_form.old_password.data):
            user.password = modify_form.new_password.data
            db.session.add(user)
            db.session.commit()
            logout_user()
            return redirect(url_for('logout'))
        else:
            flash("旧密码错误")
            return redirect(url_for('modify'))
    return render_template('modifypassword.html', modify_form=modify_form)

@app.route('/changeicon/',methods=['GET','POST'])#换头像
@login_required
def change_icon():
    user = query_user(current_user.id)
    if request.method == 'POST':
        file = request.files['file']
        path=r'.\static\icon'
        if file and allowed_iconfile(file.filename):
            file.save(os.path.join(path,file.filename))
            user.icon = '/iconfile/'+file.filename
            db.session.add(user)
            db.session.commit()
            url_for('uploaded_iconfile',filename=file.filename)
            return redirect(url_for('personal_data'))
        return '<p> 你上传了不允许的文件类型 </p>'
    return render_template('changeicon.html')

@app.route('/iconfile/<filename>')
@login_required
def uploaded_iconfile(filename):
    path = r'.\static\icon'
    return send_from_directory(path,filename)

@app.route('/uploadedvideofile/',methods=['GET','POST'])
@login_required
def uploadvideo():
    if request.method == 'POST':
        file = request.files['file']
        path=r'.\static\video'
        if file and allwoed_videofile(file.filename):
            user = query_user(current_user.id)
            file.save(os.path.join(path,file.filename))
            videoaddress='/videofile/'+file.filename
            kid = current_user.id+user.count
            user.count=str(int(user.count)+1)
            Video_=Video(id=kid,username=current_user.id,type='未分类',videoaddress=videoaddress,thumb_all=0,thumb_up=0,danmakucount=0)
            db.session.add(Video_)
            db.session.commit()
            return redirect(url_for('home'))
        return '<p> 你上传了不允许的文件类型 </p>'
    return render_template('uploadvideo.html')


@app.route('/videofile/<filename>')
@login_required
def uploaded_videofile(filename):
    path=r'.\static\video'
    return send_from_directory(path, filename)

@app.route('/myvideo/')
@login_required
def myvideo():
    video=query_video(current_user.id)
    return render_template('myvideo.html',video=video)

@app.route('/delvideo/<video_id>')
@login_required
def delvideo(video_id):
    video = Video.query.filter(Video.id==video_id).first()
    db.session.delete(video)
    comment = Comment.query.filter(Comment.video == video_id).all()
    for i in comment:
        db.session.delete(i)
    db.session.commit()
    if current_user.id=='admin':
        return redirect(url_for('admin_video'))
    return redirect(url_for('myvideo'))

@app.route('/classify/<video_id>',methods=['GET','POST'])
@login_required
def classify(video_id):
    if request.method=='POST':
        video = Video.query.filter(Video.id==video_id).first()
        type=request.values.get('type')
        video.type=type
        db.session.add(video)
        db.session.commit()
        return redirect(url_for('myvideo'))
    return render_template('classify.html')

@app.route("/videocenter/")
@login_required
def videocenter():
    page = int(request.args.get('page', 1))
    paginate = Video.query.filter(Video.id!='').paginate(page, 2, error_out=False)
    video=paginate.items
    return render_template('videocenter.html',paginate=paginate,video=video)

@app.route('/see_video/<kid>/')
@login_required
def see_video(kid):
    page = int(request.args.get('page', 1))
    commenT = Comment.query.filter(Comment.video == kid).paginate(page, 2, error_out=False)
    commentt = commenT.items
    video = Video.query.filter(Video.id == kid).first()
    thumb_up=Thumb_up.query.filter(Thumb_up.username==current_user.id).first()
    collect=Collection.query.filter(Collection.username==current_user.id,Collection.collections==video.id).first()
    return render_template('see_video.html',video=video,commenT=commenT,commentt=commentt,kid=kid,thumb_up=thumb_up,collect=collect)

@app.route('/videocenter/anime/')
@login_required
def anime():
    video = Video.query.filter(Video.type == '番剧').all()
    return render_template('anime.html',video=video)
@app.route('/videocenter/otomad/')
@login_required
def otomad():
    video = Video.query.filter(Video.type == '鬼畜').all()
    return render_template('otomad.html', video=video)
@app.route('/videocenter/film/')
@login_required
def film():
    video = Video.query.filter(Video.type == '电影').all()
    return render_template('film.html', video=video)
@app.route('/videocenter/unclassified')
@login_required
def unclassified():
    video = Video.query.filter(Video.type == '未分类').all()
    return render_template('unclassified.html',video=video)

@app.route('/comment/<kid>',methods=['GET','POST'])
@login_required
def comment(kid):
    comment_form=Comment_Form()
    video=Video.query.filter(Video.id==kid).first()
    user=User.query.filter(User.id==video.username).first()
    if request.method=='POST':
        comment=comment_form.comment.data
        kkid=user.id+user.count2
        user.count2=str(int(user.count2)+1)
        CommenT=Comment(comment=comment,id=kkid,username=current_user.id,video=kid,)
        db.session.add(CommenT)
        db.session.commit()
        return redirect(url_for('see_video',kid=kid))
    return render_template('comment.html',comment_form=comment_form,kid=video.id)


@app.route("/tm/v3/",methods=["GET","POST"])
@login_required
def tm():
    import json
    if request.method=="GET":
        #获取弹幕消息队列
        mid = request.args.get("id")
        key="movie"+str(mid)
        if rd.llen(key):
            msgs=rd.lrange(key,0,-1)
            res={
                "code":0,
                "data":[json.loads(v) for v in msgs]
            }
        else:
            res={
                "code":0,
                "data":[]
            }
        resp=json.dumps(res)
    if request.method=="POST":
        #添加弹幕
        data=json.loads(request.get_data())
        msg= {
        "__v": 0,
        "_id": datetime.datetime.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex,
        "author": data["author"],
        "time": data["time"],
        "text": data["text"],
        "color": data["color"],
        "type": data["type"],
        "ip": request.remote_addr,
        "player": data["id"]
        }
        res = {
            "code": 0,
            "danmaku":msg
        }
        resp=json.dumps(res)
        msg=[data["time"],data["type"],data["color"],data["author"],data["text"]]
        rd.lpush("movie"+str(data["id"]),json.dumps(msg))
    return Response(resp,mimetype="application/json")
@app.route('/collection/')
@login_required
def collection():
    collect=Collection.query.filter(Collection.username==current_user.id).all()
    return render_template('collection.html',collect=collect)
@app.route('/give_collection/<kid>')
@login_required
def give_collection(kid):
    video = Video.query.filter(Video.id == kid).first()
    user=query_user(current_user.id)
    id=user.id+user.count3
    user.count3=str(int(user.count3)+1)
    collec_tion=video.id
    co1=Collection(id=id,collections=collec_tion,username=current_user.id)
    db.session.add(co1)
    db.session.commit()
    return redirect(url_for('see_video',kid=kid))
@app.route('/cancle_collection/<kid>')
@login_required
def cancle_collection(kid):
    video = Video.query.filter(Video.id == kid).first()
    collect=Collection.query.filter(Collection.collections==video.id).first()
    db.session.delete(collect)
    db.session.commit()
    return redirect(url_for('see_video',kid=kid))
@app.route('/give_a_thumb-up/<kid>')
@login_required
def thumb_up(kid):
    video = Video.query.filter(Video.id == kid).first()
    video.thumb_up=str(int(video.thumb_up)+1)
    video.thumb_all=str(int(video.thumb_all)+1)
    vid=video.id
    username=current_user.id
    id=vid+video.thumb_all
    Thumb=Thumb_up(id=id,video=vid,username=username)
    db.session.add(Thumb)
    db.session.commit()
    return redirect(url_for('see_video',kid=kid))
@app.route('/cancle_a_thumb-up/<kid>')
@login_required
def cancle_thumb_up(kid):
    video = Video.query.filter(Video.id == kid).first()
    video.thumb_up=str(int(video.thumb_up)-1)
    user=Thumb_up.query.filter(Thumb_up.username==current_user.id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('see_video',kid=kid))
@app.route('/admin/')
@login_required
def admin():
    if current_user.id=='admin':
        return render_template('admin.html')
    else:
        return '您没有管理员权限'
@app.route('/admin/video')
@login_required
def admin_video():
    if current_user.id=='admin':
        video=Video.query.all()
        return render_template('admin_video.html',video=video)
    else:
        return '您没有管理员权限'
@app.route('/admin/user')
@login_required
def admin_user():
    if current_user.id=='admin':
        user=User.query.filter(User.id != 'admin').all()
        return render_template('admin_user.html',user=user)
    else:
        return '您没有管理员权限'
@app.route('/deluser/<user_id>')
@login_required
def deluser(user_id):
    deleteuser=User.query.filter(User.id==user_id).first()
    db.session.delete(deleteuser)
    deletevideo=Video.query.filter(Video.username==user_id).all()
    for i1 in deletevideo:
        db.session.delete(i1)
        ddelcommented=Comment.query.filter(Comment.video==i1.id).all()
        for k in ddelcommented:
            db.session.delete(k)
    deletecollection = Collection.query.filter(Collection.username == user_id).all()
    for i2 in deletecollection:
        db.session.delete(i2)
    deletecomment = Comment.query.filter(Comment.username == user_id).all()
    for i3 in deletecomment:
        db.session.delete(i3)
    db.session.commit()
    return redirect(url_for('admin_user'))
@app.route('/admin/comment')
@login_required
def admin_comment():
    if current_user.id=='admin':
        comments=Comment.query.all()
        return render_template('admin_comment.html',comments=comments)
    else:
        return '您没有管理员权限'
@app.route('/delcomment/<comment_id>')
@login_required
def delcomment(comment_id):
    comment=Comment.query.filter(Comment.id==comment_id).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('admin_comment'))
if __name__ == '__main__':
    app.run()