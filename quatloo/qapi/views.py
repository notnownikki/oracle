from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from qapi.serializers import QuestionSerializer
from qanda.models import Question
from qanda.parser import parse_qa
from qanda.factory import get_question, get_answer


class JSONResponse(HttpResponse):
    """
    HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class QuestionAndAnswerList(APIView):
    """
    API that takes a question and responds with a list
    of relevant questions and answers.
    """
    def get(self, request, format=None):
        questions = Question.match(request.GET.get('question'))
        serializer = QuestionSerializer(list(questions), many=True)
        return JSONResponse(serializer.data)


class NewAnswerView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        data = parse_qa(request.POST.get('qanda'))
        question = get_question(
            question_txt=data['question'], keywords=data['keywords'])
        answer = get_answer(
            question=question, answer_txt=data['answer'], url=data['url'])
        return JSONResponse(answer.id)
