from qanda.models import Question
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('question', 'answer_set')
        depth = 1
