
from app.models import Comment
from app.database import db



class CommentService():


    @staticmethod
    def add_comment(name, email, comments, post_id):
        comment = Comment(post_id=post_id, name=name, email=email, comments=comments)

        db.session.add(comment)
        db.session.commit()


    @staticmethod
    def get_comments(post_id):

        comments = Comment.query.filter_by(post_id=post_id).all()
        if len(comments):
            return [comment.to_dict() for comment in comments]
        else:
            return []


    @staticmethod
    def delete_comments(post_id):
        comments = Comment.query.filter_by(post_id=post_id).all()
        if comments is not None:
            for comment in comments:
                db.session.delete(comment)

            db.session.commit()

    @staticmethod
    def get_comments_count(post_id):

        comments = Comment.query.filter_by(post_id=post_id).all()

        return len(comments)

