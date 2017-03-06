from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class QuestionAndAnswerList(APIView):
	"""
	API that takes a question and responds with a list
	of relevant questions and answers.
	"""
	def get(self, request, format=None):
		questions = Question.objects.match(request.GET.get('question'))
