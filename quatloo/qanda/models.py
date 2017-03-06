from django.db import models


class Question(models.Model):
    question = models.TextField()
    keywords = models.TextField()

    @staticmethod
    def match(question):
        """
        Matches an asked question with a questions in the database that might
        be appropriate, based on a full text search.
        """
        return Question.objects.raw(
            """
            SELECT *, MATCH(question, keywords) AGAINST
                (%s IN NATURAL LANGUAGE MODE) AS score
            FROM qanda_question
            WHERE MATCH(question, keywords) AGAINST
                (%s IN NATURAL LANGUAGE MODE)
            ORDER BY score DESC
            """, [question, question]
        )


class Answer(models.Model):
    question = models.ForeignKey(Question)
    # where to find the solution
    url = models.URLField()
    # extra answer detail
    answer = models.TextField()
