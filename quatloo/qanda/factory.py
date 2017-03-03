import re
from qanda.models import Question, Answer


def get_question(question_txt, keywords):
    question, _ = Question.objects.get_or_create(question=question_txt)

    keywords = set(
        [keyword for keyword in re.split('\W+', keywords or '')
         if keyword != ''])
    existing_keywords = set(
        [keyword for keyword in re.split('\W+', question.keywords or '')
         if keyword != ''])

    if keywords and keywords != existing_keywords:
        existing_keywords.update(keywords)
        existing_keywords = list(existing_keywords)
        existing_keywords.sort()
        question.keywords = ', '.join(existing_keywords)
        question.save()

    return question


def get_answer(question, answer_txt, url):
    # does an answer exist for this question with this url?
        # update the answer text if any was supplied
    # else, create new answer for this question
    pass
