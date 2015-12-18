from .database import db

from datetime import datetime


class User(db.Model):
 
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(100), unique=True)

    # account need to be confirmed by email
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    # account create time and update
    createdAt = db.Column(db.DateTime, default = datetime.now())
    updatedAt = db.Column(db.DateTime, default = datetime.now())

    def to_dict(self):
        return dict(
            id = self.id,
            username = self.username,
            email = self.email,
            confirmed = self.confirmed

        )


class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), primary_key=True)


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def to_dict(self):
        return dict(
            id = self.id,
            name = self.name
        )

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

articles_tags = db.Table(
    'articles_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('post.id'))
)

class Post(db.Model):

    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text)

    createAt = db.Column(db.DateTime, default=datetime.now())
    updateAt = db.Column(db.DateTime, default=datetime.now())

    #user_id = db.Column(db.Integer)

    # 将文章关联到用户
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref = db.backref('user_post', lazy='dynamic'))

    # 文章标签
    tags = db.relationship('Tag', secondary=articles_tags, backref=db.backref('post', lazy='dynamic'))

    def to_dict(self):
        return dict(
            id = self.id,
            title = self.title,
            content = self.content,
            createAt = self.createAt,
            updateAt = self.updateAt,
            tags = self.tags
        )

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self


class Comment(db.Model):

    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=True)

    comments = db.Column(db.Text)
    createdAt = db.Column(db.DateTime, default=datetime.now())


    # 将评论绑定到相关文章
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref = db.backref('post_comment', lazy='dynamic'))


    def to_dict(self):
        return dict(
            id = self.id,
            name = self.name,
            email = self.email,
            comments = self.comments,
            createAt = self.createdAt

        )


