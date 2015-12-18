
from flask import render_template, url_for, request, redirect, session, flash


from app.forms import SignupForm
from app.services import UserService
from app.services.email import send_email
from app.database import db
from app.utils.auth import login_required, logout_admin



from . import bp



#@bp.route('/')
#def index():
#    return render_template('admin/signin.html')


@bp.route('/signup', methods=['GET', 'POST'])
def signup():

    #if 'admin_uid'  in session:
    #    return render_template('admin/index.html', username=session['admin_uid'])

    if request.method == 'GET':
        return render_template('admin/SignUp.html')

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')


    try:
        UserService.add_user(username, password, email)
    except Exception as e:
        print(e)

    token = UserService.generate_email_token(email)
    confirmUrl = url_for('admin.confirm_email', token=token, external=True)

    #html = render_template('admin/email.html', confirm_url = confirmUrl)


    subject = 'Please confirm your address'
    sender = 'admin'
    #send_email(subject, sender, user['email'], html)

    # return render_template('admin/signin.html', form)
    return redirect(url_for('admin.signin'))



@bp.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = UserService.verify_email_token(token)
    except:
        flash('The confirm Url is invalid!')

    user = UserService.get_by_email(email['email'])

    if user['confirmed']:
        flash('The account has been confirmed!')
    else:
        UserService.update_confirmed_user(email('email'))
        flash('The account is confirmed, redirect to login')

    return redirect(url_for('admin.signin'))


@bp.route('/signin', methods=['GET', 'POST'])
def signin():

    if 'admin_uid'  in session:
        #return render_template('admin/index.html', username=session['admin_uid'])
        return redirect(url_for('admin.index'))

    if request.method == 'GET':
        return render_template('admin/login.html')

    email = request.form.get('email')
    password = request.form.get('password')


    if UserService.check_password(email, password):
        session.permanent = True

        # session input the username 。。
        user = UserService.get_by_email(email)
        session['admin_uid'] = user['username']

        return redirect(url_for('admin.index'))

    else:
        return render_template('admin/login.html')


@bp.route('/logOut')
@login_required
def logOut():
    logout_admin()

    return redirect(url_for('admin.signin'))

