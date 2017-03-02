from django.test import TestCase
from qanda.parser import parse_qa, ParserError


class QAParserTestCase(TestCase):
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
            'keywords': '(themes, style, styles)',
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
