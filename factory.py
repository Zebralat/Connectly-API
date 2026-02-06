from .models import Post

class PostFactory:
    @staticmethod
    def create_post(author_id, content):
        # This factory handles the logic of creating a post
        if not content:
            raise ValueError("Content cannot be empty")
        return Post.objects.create(author_id=author_id, content=content)