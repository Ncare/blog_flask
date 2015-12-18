
from flask import render_template, redirect, request, url_for, session, flash, jsonify, abort
from app.services import PostService, CommentService
from app.forms import PostForm
from app.utils.auth import login_required
from app.utils.helper import generate_page

from config import POSTS_PER_PAGE, POSTS_PER_PAGE_BACK
from .import bp


import json



@bp.route('/')
#@bp.route('/index')
@login_required
def index():

    # 应该判定一下 admin_uid 是否在表中
    if session.get('admin_uid'):
        return render_template('admin/index.html', username=session['admin_uid'])
    else:
        return redirect(url_for('admin.signin'))


@bp.route('/preview', methods=['GET', 'POST'])
def test():

    # for keep the value in last post by jquery .ajx
    global pTitle
    global pContent

    if request.method == 'POST':
        data = request.json

        pTitle = data['title']
        pContent = data['content']
    else:
        return render_template('admin/preview.html', title=pTitle, content=pContent)


@bp.route('/posts')
#@bp.route('/posts/<int:page>')
def show_posts(page = 1):

    #posts = PostService.get_posts()
    #posts, nav = PostService.get_posts_paginate(page, POSTS_PER_PAGE, False)

    #return  render_template('admin/posts.html', posts = posts, nav=nav, username=session['admin_uid'])

        # 实现分页 1， 2， 3， 4 。。。
    page = request.args.get("page", 1)

    offset = POSTS_PER_PAGE*(int(page)-1)
    postList = PostService.get_posts_page(offset, POSTS_PER_PAGE_BACK)
    pager = generate_page(PostService.get_posts_count(), POSTS_PER_PAGE_BACK, int(page))


    # 超出页面，
    if int(page)>pager['sumPage'] and pager['sumPage']!=0:
        abort(404)

    #comCount = [CommentService.get_comments_count(post['id']) for post in postList]
    return render_template('admin/posts.html', posts=postList, pager=pager)



@bp.route('/posts/<int:id>')
def post(id):
    post = PostService.get_one(id)
    comment = CommentService.get_comments(id)

    return render_template('admin/posts.html', post=post, comment=comment)


@bp.route('/posts/add', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'GET':
        return render_template('admin/add_post.html')

    title = request.form['title']
    content = request.form['content']
    tags = request.form['tags']

    tagsList = [item.strip() for item in tags.split(',')]

    try:
        post = PostService.add_post(title, content, tagsList)
        flash('add success')
        print('success')
    except:
        flash('add failed')

    return render_template('admin/index.html')


#@bp.route('/posts/<int:id>/delete')
#def delete_post(id):
#    try:
#        PostService.delete_post(id)
#        CommentService.delete_comments(id)
#    except:
#        return render_template('admin/posts.html')
#
#    return redirect(url_for('admin.index'))



# 异步提交删除
@bp.route('/delete', methods=['GET','POST'])
@login_required
def delete():

    if request.method == 'POST':
        data = request.json
        print(data)

        try:
            PostService.delete_post(data['post_id'])
            CommentService.delete_comments(data['post_id'])
        except Exception as e:
            print(e)
            return json.dumps({'has_error':True, 'message':"删除错误"})

        return jsonify(success=True, message="删除成功" )




@bp.route('/posts/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = PostService.get_one(id)

    print(post)
    form = PostForm(title=post.get('title'), content=post.get('content'))
    if request.method == 'GET':
        return render_template('admin/update.html', form=form, post = post)

    title = request.form['title']
    content = request.form['content']


    dic = {'title':title, 'content':content}
    try:
        post= PostService.update_post(id, dic)
        print("success")
        flash('update success')
    except:
        flash('update failed')

    return redirect(url_for('admin.show_posts'))



@bp.route('/showComment', methods=['GET', 'POST'])
def showComments():

    if request.method == 'POST':
        data = request.json

        try:
            comments = CommentService.get_comments(post_id=data['id'])
            count = CommentService.get_comments_count(post_id=data['id'])
        except:
            return json.dumps({'has_error':True, 'message':"查询出错"})


        if not count:
            return jsonify(success=True, count=0, message="没有评论")
        else:
            return  jsonify(success=True, count=count, info=comments)









