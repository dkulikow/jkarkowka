from django.contrib.auth.models import User
from api.models import Student, Question, Answer, SolvedTest, Test, Group, Lecturer, SubmittedAnswer
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class LecturerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lecturer
        fields = ('name',)


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ('content', 'good')


class HiddenAnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'content')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'content', 'answers')


class ShortQuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ('content',)


class QuestionWithoutAnswerSerializer(serializers.HyperlinkedModelSerializer):
    answers = HiddenAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'content', 'answers')


class TestSerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ('id', 'key', 'name', 'questions')


class ShortTestSerializer(serializers.HyperlinkedModelSerializer):
    questions = ShortQuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ('id', 'name', 'questions')


class TestStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Test
        fields = ('id',)


class TestWithHiddenAnswersSerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionWithoutAnswerSerializer(many=True)

    class Meta:
        model = Test
        fields = ('id', 'name', 'questions')


class SubmittedAnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubmittedAnswer
        fields = ('answer',)


class SolvedTestSerializer(serializers.HyperlinkedModelSerializer):
    test = ShortTestSerializer(many=False)
    answers = SubmittedAnswerSerializer(many=True)

    class Meta:
        model = SolvedTest
        fields = ('test', 'answers')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    solved_tests = SolvedTestSerializer(many=True)

    class Meta:
        model = Student
        fields = ('user', 'solved_tests')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    lecturer = LecturerSerializer()
    students = StudentSerializer(many=True)
    activated_tests = TestStateSerializer(many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'lecturer', 'students', 'activated_tests')