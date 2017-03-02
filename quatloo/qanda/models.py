from django.db import models


class Question(models.Model):
    question = models.TextField()
    keywords = models.TextField()


class Answer(models.Model):
    question = models.ForeignKey(Question)
    # where to find the solution
    url = models.UrlField()
    # extra answer detail
    answer = models.TextField()
