from app.models import Tag, articles_tags
from app.database import db



class TagService():

    @staticmethod
    def get_all_tags():
        tags = Tag.query.all()
        return [tag.to_dict() for tag in tags]


    @staticmethod
    def get_tag_byId(id):
        tag = Tag.query.get(id)
        print(tag)


    @staticmethod
    def get_post_byTag(tag):
        id = Tag.query.filter_by(name=tag).first()
        posts = id.post.all()
        return [post.to_dict() for post in posts]