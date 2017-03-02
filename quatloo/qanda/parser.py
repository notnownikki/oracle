import re

URL_RE = re.compile('.*(https?:\/\/([\da-z\.-]+\.([a-z\.]{2,6})([\/\w \.-]*)*\/?)?)$')
KEYWORDS_RE = re.compile('(\(.*\))')

class ParserError(Exception):
    pass


def parse_qa(qa):
    if '?' not in qa:
        raise ParserError()

    qa = qa.strip()

    # extract the url at the end
    match = URL_RE.match(qa)
    if match:
        url = match.groups()[0]
        qa = qa[0:-len(url)]
    else:
        url = ''

    # extract the question
    question = qa.split('?')[0].strip() + '?'
    qa = qa.split('?')[1].strip()

    # extract any keywords
    match = KEYWORDS_RE.match(qa)
    if match:
        keywords = match.groups()[0]
        qa = qa.replace(keywords, '').strip()
    else:
        keywords = ''

    # what's left is answer text
    answer = qa.strip()

    return {
        'question': question,
        'keywords': keywords,
        'answer': answer,
        'url': url
    }
