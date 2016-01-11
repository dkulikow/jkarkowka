from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Student, Question, SolvedTest, Test
from api.serializers import GroupSerializer, UserSerializer, StudentSerializer, QuestionSerializer, SolvedTestSerializer, TestSerializer
from rest_framework.decorators import api_view, parser_classes, detail_route
from rest_framework.parsers import JSONParser


def index(request):
    return HttpResponse("Hello, world!")


@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
def tests(request):
    queryset = Test.objects.all()
    if request.method == 'POST':
        data = request.data
        if data["method"] == "list":
            if "id" in data:
                id = request.data["id"]
                queryset = Test.objects.filter(id__exact=id)
        serializer = TestSerializer(queryset, many=True, context={'request': request})
        data = request.data
        return Response(serializer.data)
    if request.method == 'GET':
        serializer = TestSerializer(queryset, many=True, context={'request': request})
        data = request.data
    return Response(serializer.data)


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


