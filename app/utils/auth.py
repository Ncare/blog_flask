
from functools import wraps
from flask import session, redirect, url_for


def login_admin(user_id):
    session.permanent = True
    session['admin_uid'] = user_id


def logout_admin():
    session.pop('admin_uid', None)



# 需要登录
def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if 'admin_uid' not in session:
            return  redirect(url_for('admin.signin'))
        return func(*args, **kwargs)
    return decorated

