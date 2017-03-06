from django.test import TestCase, SimpleTestCase
from qanda.parser import parse_qa, ParserError
from qanda.models import Question, Answer
from qanda.factory import get_question, get_answer


class QAParserTestCase(SimpleTestCase):
    def test_extract_question_and_url(self):
        qa = 'How do I do the thing? http://learntodoathing.com/'
        expected = {
            'question': 'How do I do the thing?',
            'keywords': '',
            'url': 'http://learntodoathing.com/',
            'answer': ''
        }
        self.assertEqual(parse_qa(qa), expected)

    def test_extract_question_and_answer(self):
        qa = 'How do I do the thing? You must believe you can do the thing.'
        expected = {
            'question': 'How do I do the thing?',
            'keywords': '',
            'url': '',
            'answer': 'You must believe you can do the thing.'
        }
        self.assertEqual(parse_qa(qa), expected)

    def test_extract_question_answer_url(self):
        qa = 'How do I do the thing? Believe you can! http://doathing.com/'
        expected = {
            'question': 'How do I do the thing?',
            'keywords': '',
            'url': 'http://doathing.com/',
            'answer': 'Believe you can!'
        }
        self.assertEqual(parse_qa(qa), expected)

    def test_questions_and_answers_can_talk_about_http(self):
        qa = 'How do I redirect from https to https? Just redirect from http to https.  http://beggingthequestion.com/'
        expected = {
            'question': 'How do I redirect from https to https?',
            'keywords': '',
            'url': 'http://beggingthequestion.com/',
            'answer': 'Just redirect from http to https.'
        }
        self.assertEqual(parse_qa(qa), expected)

    def test_keywords_are_added_to_the_question(self):
        qa = 'How do I change the theme? (themes, style, styles) Use our handy tool! https://example.com/'
        expected = {
            'question': 'How do I change the theme?',
            'keywords': 'themes, style, styles',
            'url': 'https://example.com/',
            'answer': 'Use our handy tool!'
        }
        self.assertEqual(parse_qa(qa), expected)

    def test_fields_stripped_of_whitespace(self):
        qa = '  How do I do the thing ? Believe you can!   http://doathing.com/ '
        expected = {
            'question': 'How do I do the thing?',
            'keywords': '',
            'url': 'http://doathing.com/',
            'answer': 'Believe you can!'
        }
        self.assertEqual(parse_qa(qa), expected)

    def test_only_question(self):
        qa = 'How do I do the thing?'
        expected = {
            'question': 'How do I do the thing?',
            'keywords': '',
            'url': '',
            'answer': ''
        }
        self.assertEqual(parse_qa(qa), expected)

    def test_no_question(self):
        qa = 'I liek chocolate milk'
        self.assertRaises(ParserError, parse_qa, qa)


class QuestionFactoryTestCase(TestCase):
    def test_new_question(self):
        question = get_question(
            question_txt='How do I do a thing?', keywords='stuff, things')
        self.assertEqual(question.question, 'How do I do a thing?')
        self.assertEqual(question.keywords, 'stuff, things')

    def test_update_question_keywords(self):
        question = Question.objects.create(
            question='How do I do a thing?', keywords='things, stuff')
        question = get_question(
            question_txt='How do I do a thing?', keywords='jam, cakes')
        self.assertEqual(question.keywords, 'cakes, jam, stuff, things')


class AnswerFactoryTestCase(TestCase):
    def test_new_answer(self):
        question = Question.objects.create(
            question='How do I do a thing?', keywords='things, stuff')
        answer = get_answer(
            question=question, url='http://example.com/',
            answer_txt='Here is an example.')
        self.assertEqual(answer.question, question)
        self.assertEqual(answer.url, 'http://example.com/')
        self.assertEqual(answer.answer, 'Here is an example.')
        self.assertEqual(Answer.objects.all().count(), 1)

    def test_new_answer_with_empty_url(self):
        question = Question.objects.create(
            question='How do I do a thing?', keywords='things, stuff')
        answer = get_answer(
            question=question, answer_txt='Here is an example.', url='')
        self.assertEqual(answer.question, question)
        self.assertEqual(answer.url, '')
        self.assertEqual(answer.answer, 'Here is an example.')
        self.assertEqual(Answer.objects.all().count(), 1)

    def test_additional_answer(self):
        question = Question.objects.create(
            question='How do I do a thing?', keywords='things, stuff')
        Answer.objects.create(
            question=question, url='http://example.com/',
            answer='Here is an example.')
        answer = get_answer(
            question=question, url='http://other-example.com/',
            answer_txt='Here is another example.')
        self.assertEqual(answer.question, question)
        self.assertEqual(answer.url, 'http://other-example.com/')
        self.assertEqual(answer.answer, 'Here is another example.')
        self.assertEqual(Answer.objects.all().count(), 2)

    def test_answer_text_updated(self):
        question = Question.objects.create(
            question='How do I do a thing?', keywords='things, stuff')
        Answer.objects.create(
            question=question, url='http://example.com/',
            answer='Old answer')
        answer = get_answer(
            question=question, url='http://example.com/',
            answer_txt='Here is an example.')
        self.assertEqual(answer.question, question)
        self.assertEqual(answer.url, 'http://example.com/')
        self.assertEqual(answer.answer, 'Here is an example.')
        self.assertEqual(Answer.objects.all().count(), 1)

    def test_answer_text_not_updated_if_blank(self):
        question = Question.objects.create(
            question='How do I do a thing?', keywords='things, stuff')
        Answer.objects.create(
            question=question, url='http://example.com/',
            answer='Old answer')
        answer = get_answer(
            question=question, url='http://example.com/',
            answer_txt='')
        self.assertEqual(answer.question, question)
        self.assertEqual(answer.url, 'http://example.com/')
        self.assertEqual(answer.answer, 'Old answer')
        self.assertEqual(Answer.objects.all().count(), 1)


class QuestionMatchTestCase(SimpleTestCase):
    """
    We need to override Django's transaction handling to make sure
    the fulltext index is used when we insert test data.
    """
    allow_database_queries = True

    def tearDown(self):
        super(QuestionMatchTestCase, self).tearDown()
        Question.objects.all().delete()

    def test_match_against_question(self):
        question = Question(
            question='How do I make a widget?',
            keywords='custom, widgets, easteregg')
        question.save()
        questions = Question.match('I want to make a widget.')
        self.assertEqual(1, len(list(questions)))
        self.assertEqual(question.id, questions[0].id)

    def test_match_against_keywords(self):
        question = Question(
            question='How do I make a widget?',
            keywords='custom, widgets, easteregg')
        question.save()
        questions = Question.match('Show an easteregg please.')
        self.assertEqual(1, len(list(questions)))
        self.assertEqual(question.id, questions[0].id)
