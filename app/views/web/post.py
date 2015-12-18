
from flask import render_template, redirect, url_for, session, request, flash, jsonify, g, abort

from app.services.post import PostService
from app.services.comment import CommentService
from app.services.tag import TagService

from app.forms import CommentForm

from config import POSTS_PER_PAGE
from app.utils.helper import generate_page

import json
from datetime import datetime


from . import fp



@fp.route('/')
@fp.route('/index')
#@fp.route('/index/<int:page>')
def index():

    # 实现分页 1， 2， 3， 4 。。。
    page = request.args.get("page", 1)

    offset = POSTS_PER_PAGE*(int(page)-1)
    postList = PostService.get_posts_page(offset, POSTS_PER_PAGE)
    pager = generate_page(PostService.get_posts_count(), POSTS_PER_PAGE, int(page))

    # 超出页面，
    if int(page)>pager['sumPage'] and pager['sumPage']!=0:
        abort(404)

    comCount = [CommentService.get_comments_count(post['id']) for post in postList]

    postsZip = zip(postList, comCount)

    posts_recent = PostService.get_posts_recent(4, 'desc')

    return render_template('web/index.html', posts=postsZip, pager=pager, postR = posts_recent)



    #posts = PostService.get_posts()
    # 实现了分页
    #posts, nav = PostService.get_posts_paginate(page, POSTS_PER_PAGE, False)

    #posts_recent = PostService.get_posts_recent(4, 'desc')

    # 获取评论数
    #comCount = [CommentService.get_comments_count(post['id']) for post in posts]

    #postsZip = zip(posts, comCount)

    #return render_template('web/index.html', posts=postsZip, postR = posts_recent, nav=nav)


@fp.route('/test')
def test():

    return render_template('web/test.html')




@fp.route('/posts/<int:id>', methods = ['GET', 'POST'])
def post(id):

    #cForm = CommentForm(request.form)
    post = PostService.get_one(id)


    tags = [item.name for item in post['tags']]

    try:
        comments = CommentService.get_comments(int(id))
    except Exception:
        print(Exception)

    commentCount = len(comments)

    # get pre or next page
    try:
        next = PostService.get_next_post(id)
        if next is not None:
            nextId = next.id
        else:
            nextId = None
        pre = PostService.get_pre_post(id)
        if pre is not None:
            preId = pre.id
        else:
            preId = None
    except Exception as e:
        print(e)

    # get tag

    #if request.method == "GET":
    return render_template('web/post.html', post=post, cs = comments, count = commentCount, \
            nextPostId = nextId, prePostId = preId, tags = tags)


    #print(cForm.validate_on_submit())


    #post_id = int(id)
    #name = request.form.get('name')
    #email = request.form.get('email')
    #commentText = request.form.get('Text')


    #try:
    #    ct = CommentService.add_comment(name=name, email=email, comments=commentText, post_id=post_id)
    #    print('add a comment successful')
    #except:
    #    print('failed !')


    #return render_template('web/post.html', post=post, cs=comments)


# 评论无刷新
@fp.route('/comment', methods=['GET', 'POST'])
def comment():

    if request.method == 'POST':
        comment = request.json

        name = comment['name']
        email = comment['email']
        comContent = comment['comment']
        post_id = comment['post_id']

        post = PostService.get_one(post_id)

        if not post:
            return json.dumps({'has_error':True, "message":"文章不存在"})

        try:
            CommentService.add_comment(post_id=post_id, name=name, email=email, comments=comContent)
        except:
            return json.dumps({'has_error':True, "message":"存取出错"})

        return jsonify(success=True, message="评论成功", time=datetime.utcnow())




@fp.route('/tags')
def tags():

    tags = TagService.get_all_tags()
    print(tags)
    return render_template('web/tag.html', tags=tags)


@fp.route('/tags/<string:tag>')
def tagList(tag):

    posts = TagService.get_post_byTag(tag)

    return render_template('web/taginfo.html', posts=posts)

@fp.route('/about')
def about():

    return render_template('web/about.html')



# search function
@fp.route('/search/', methods = ['GET', 'POST'])
def search():

    print(request)
    if "keyword" in request.args:
        keyword = request.args['keyword'].split()
        matchPost = PostService.text_search(keyword)

    count = len(matchPost)

    return render_template('web/search.html', posts = matchPost, count=count)

