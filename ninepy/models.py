from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    media = models.ImageField(upload_to='ninepy/')
    publication_date = models.DateTimeField('date published')
    author_name = models.CharField(max_length=50)
    vote_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    content = models.CharField(max_length=200)
    publication_date = models.DateTimeField('date published')
    author_name = models.CharField(max_length=50)
    post = models.ForeignKey('Post', null=True, blank=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.author_name