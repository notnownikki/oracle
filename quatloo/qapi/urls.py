from qapi.views import QuestionAndAnswerList, NewAnswerView

question_match = QuestionAndAnswerList.as_view()
answer = NewAnswerView.as_view()
