from flask import render_template
from . import type_blue  # 导入蓝图对象
from app.utils.common import login_required  # 引入装饰器


@type_blue.route('/admin/type')
@login_required
def index():
    return render_template('admin/type/index.html')
