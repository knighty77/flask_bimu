from flask import render_template, request, jsonify, json, flash, redirect, session, make_response
from werkzeug.security import generate_password_hash
from . import admin_blue
from app.models import User
from app import db
import re
from app.utils.common import login_required
from app.utils.captcha.captcha import captcha
from app import redis_store, constants


@admin_blue.route('/admin')
@login_required
def index():
    return render_template('admin/index/index.html')


# 后台注册
@admin_blue.route('/admin/user/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        if not data['username']:
            return jsonify(status=0, msg='请填写用户名')
        if not data['password']:
            return jsonify(status=0, msg='请填写密码')

        if data['check_password'] != data['password']:
            return jsonify(status=0, msg='两次密码输入不一致')

        if not re.match(r'1[3456789]\d{9}$', data['mobile']):
            return jsonify(status=0, msg='手机号格式错误')

        # 根据手机号进行查询，确认用户是否注册
        user_mobile = User.query.filter_by(mobile=data['mobile']).first()
        if user_mobile:
            return jsonify(status=0, msg='手机号码已被注册')

        # 构造模型类对象，准备存储数据到 user 表中
        user = User()
        user.mobile = data['mobile']
        user.username = data['username']
        user.password = generate_password_hash(data['password'])
        # 把用户数据提交到数据库中
        db.session.add(user)
        db.session.commit()

        return jsonify(status=1, msg='注册成功')
    else:
        return render_template('admin/user/register.html')


@admin_blue.route('/admin/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        captcha = request.form['captcha']  # 接收前端提交过来的验证码
        image_code_id = request.form['image_code_id']  # 接收前端提交过来的 image_code_id
        real_image_code = str(redis_store.get('ImageCode_' + image_code_id))  # 把image_code_id转成字符串，然后存入redis

        # print(real_image_code.lower())
        if real_image_code.lower() != captcha.lower():
            flash('图片验证码不一致')
            return redirect(request.referrer)

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('用户名或密码错误')
            return redirect(request.referrer)

        session['user'] = user
        return redirect('/admin')

    return render_template('admin/user/login.html')


# 后台退出
@admin_blue.route('/admin/logout')
def logout():
    # 退出本质就是清除session
    session.pop("user")
    return redirect('/admin/user/login')  # 退出后跳转到登录


@admin_blue.route('/admin/image_code')
def generate_image_code():
    image_code_id = request.args.get('image_code_id')  # 获取参数
    if not image_code_id:  # 判断参数是否存在
        return jsonify(status=0, msg='参数缺失')
    name, text, image = captcha.generate_captcha()  # 调用扩展来生成图片验证码

    redis_store.setex('ImageCode_' + image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)

    response = make_response(image)  # 使用响应对象返回图片本身
    response.headers['Content-Type'] = 'image/jpg'  # 设置响应的数据类型
    return response  # 返回响应


@admin_blue.route('/admin/user/settings', methods=['GET', 'POST'])
def settings():
    user = session.get('user')
    if request.method == 'POST':
        used_password = request.form['used_password']
        password = request.form['password']
        check_password = request.form['check_password']
        if not user.check_password(used_password):
            flash('密码输入错误')
            return redirect(request.referrer)
        if password != check_password:
            flash('两次输入密码不一致')
            return redirect(request.referrer)
        user = User.query.filter_by(id=user.id).first()
        user.password = generate_password_hash(password)
        db.session.commit()
        session.pop('user')
        return redirect('/admin/user/login')
    return render_template('admin/user/settings.html')
