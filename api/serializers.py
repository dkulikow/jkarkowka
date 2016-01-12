from django.contrib.auth.models import User
from api.models import Student, Question, Answer, SolvedTest, Test, Group, Lecturer
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


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('content', 'type', 'answers')


class ShortQuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ('content',)


class TestSerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ('id', 'state', 'key', 'name', 'questions')


class ShortTestSerializer(serializers.HyperlinkedModelSerializer):
    questions = ShortQuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ('name', 'questions')


class SolvedTestSerializer(serializers.HyperlinkedModelSerializer):
    test = ShortTestSerializer(many=False)
    answers = AnswerSerializer(many=True)

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

    class Meta:
        model = Group
        fields = ('name', 'lecturer', 'students')