from src.models.post import Post, db

class PostRepository:
    def get_all_posts(self):
        return Post.query.all()

    def get_post_by_id(self, post_id):
        return Post.query.filter_by(id=post_id).first()

    def create_post(self, **kwargs):
        post = Post(**kwargs)
        db.session.add(post)
        db.session.commit()
        return post

    def update_post(self, post_id, **kwargs):
        post = self.get_post_by_id(post_id)
        if post:
            for key, value in kwargs.items():
                setattr(post, key, value)
            db.session.commit()
            return post
        else:
            raise ValueError(f'Post with id {post_id} not found')

    def delete_post(self, post_id):
        post = self.get_post_by_id(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return True
        else:
            raise ValueError(f'Post with id {post_id} not found')