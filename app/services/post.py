
from app.models import Post, Tag
from app.database import db



class PostService():


    @staticmethod
    def get_posts():
        posts = Post.query.order_by('id').all()
        return [post.to_dict() for post in posts]


    # 分页功能 prv and next
    @staticmethod
    def get_posts_paginate(start, perPage, status):
        nav = Post.query.order_by('id').paginate(start, perPage, status)
        posts = nav.items
        return [post.to_dict() for post in posts], nav

    # 分页功能 1， 2， 3， 4
    @staticmethod
    def get_posts_page(offset, perPage):
        allPost = Post.query.order_by(Post.createAt.desc())
        try:
            pagePost = allPost.limit(perPage).offset(offset).all()
        except Exception as e:
            print(e)
        return [post.to_dict() for post in pagePost]

    # 获取post的数量
    @staticmethod
    def get_posts_count():
        count = Post.query.count()
        return count

    @staticmethod
    def get_posts_recent(num, mode):
        if mode == 'desc':
            posts = Post.query.order_by(Post.updateAt.desc()).limit(num)
        else:
            posts = Post.query.order_by(Post.updateAt.asc()).limit(num)
        return [post.to_dict() for post in posts]

    @staticmethod
    def get_one(post_id):

        post = Post.query.filter_by(id=post_id).first()

        if post:
            return post and post.to_dict()
        else:
            return False

    @staticmethod
    def add_post(title, content=None, tagnames=[]):
        post = Post(title=title, content=content)
        for tagname in tagnames:
            tag = db.session.query(Tag).filter(Tag.name==tagname).first()
            if not tag:
                tag = Tag(name=tagname)
                tag.save()
            post.tags.append(tag)

        post.save()


    @staticmethod
    def delete_post(post_id):
        # 把相关的标签索引也删除掉了
        post = Post.query.get(post_id)
        post.delete()


    @staticmethod
    def update_post(post_id, update_info):
        post = Post.query.get(post_id)
        for k, v in update_info.items():
            if v is not None:
                setattr(post, k, v)

        db.session.add(post)
        db.session.commit()


    @staticmethod
    def get_next_post(id):
        next = db.engine.execute('SELECT * FROM `post` where id>%s order by updateAt asc' % id).first()
        return next

    @staticmethod
    def get_pre_post(id):
        pre = db.engine.execute('SELECT * FROM `post` where id<%s order by updateAt desc' % id).first()
        return pre


    @staticmethod
    def text_search(keyword):
        matchAll = []
        for word in keyword:
            match = Post.query.filter(Post.content.ilike("%" + word + "%")).all()
            matchAll += match
        return [post.to_dict() for post in matchAll]