from django.db import models


class CustomUser(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    bio = models.TextField()

    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=50)  # Name of the tag

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='tags')

    class Meta:
        indexes = [
            models.Index(fields=['author']),  # Index on author for optimized filtering
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['post', 'created_at']),  # Composite index on post and created_at
        ]

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'