import json

from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Student, Question, SolvedTest, Test, Group, Lecturer
from api.serializers import GroupSerializer, UserSerializer, StudentSerializer, QuestionSerializer, SolvedTestSerializer, TestSerializer, \
    ShortTestSerializer, TestWithHiddenAnswersSerializer
from rest_framework.decorators import api_view, parser_classes, detail_route
from rest_framework.parsers import JSONParser


def index(request):
    return HttpResponse("Hello, world!")


@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
def tests(request):
    queryset = Test.objects.all()
    data = request.data # typ dict
    serializer = TestSerializer(queryset, many=True, context={'request': request})
    if request.method == 'POST':
        if data["method"] == "list":
            if "id" in data:
                id = data["id"]
                queryset = Test.objects.filter(id__exact=id)
                serializer = TestSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)
        if data["method"] == "get_test":
            if "test_id" in data:
                test_id = data["test_id"]
                queryset = Test.objects.filter(id__exact=test_id)
                serializer = TestWithHiddenAnswersSerializer(queryset, many=True, context={'request': request})
                return Response(serializer.data)
        if data["method"] == "get_key":
            if "test_id" in data:
                test_id = data["test_id"]
                queryset = Test.objects.filter(id__exact=test_id).values('key')
                serializer = TestSerializer(queryset, many=True, context={'request': request})
                return Response(queryset)
        if data["method"] == "change_state":
            test_id = data["test_id"]
            if "students_id" in data:
                students_id = data["students_id"]
            elif "group_id" in data:
                group_id = data["group_id"]
            state = data["state"]
            test = Test.objects.get(id__exact=test_id)
            test.state = state
            test.save()
            return HttpResponse()
        if data["method"] == "send":
            test_id = data["test_id"]
            answers = data["answers"]
            if request.user.is_authenticated():
                username = request.user.username
            return HttpResponse(username + " " + test_id + " " + ' '.join(answers))
    if request.method == 'GET':
        serializer = TestSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
def questions(request):
    data = request.data # typ dict
    if request.method == 'POST':
        queryset = Question.objects.all().values('id','content')
        if data["method"] == "list":
            if "id" in data:
                id = data["id"]
                queryset = Question.objects.filter(id__exact=id).values('id','content')
        return Response(queryset)
    if request.method == 'GET':
        queryset = Question.objects.all()
        serializer = QuestionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
def groups(request):
    data = request.data # typ dict
    queryset = Group.objects.all()
    if request.method == 'POST':
        if data["method"] == "list":
            if "id" in data:
                id = data["id"]
                queryset = Group.objects.filter(id__exact=id)
        serializer = GroupSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    if request.method == 'GET':
        serializer = GroupSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    return Response(queryset)


@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
def user(request):
    data = request.data # typ dict
    response_data = {}
    response_data['result'] = 'error'
    if request.method == 'POST':
        if data["method"] == "about":
            username = request.user.username
            student_queryset = Student.objects.filter(user__username=username)
            lecturer_queryset = Lecturer.objects.filter(user__username=username)
            if student_queryset.count() > 0:
                response_data['result'] = '1'
            elif lecturer_queryset.count() >0:
                response_data['result'] = '0'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class SolvedTestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SolvedTest.objects.all()
    serializer_class = SolvedTestSerializer


