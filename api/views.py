import json

from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response

from api.models import *
from api.serializers import *
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
                key = Test.objects.get(id__exact=test_id).key
                print(type(key))
                response_data = [{"key": key}]
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        if data["method"] == "change_state":
            test_id = data["test_id"]
            test = Test.objects.get(id__exact=test_id)
            state = data["state"]
            if state == "1":
                if "students_id" in data:
                    students_id = data["students_id"]
                    for student_id in students_id:
                        student = Student.objects.get(id__exact=student_id)
                        activated_relation = ActiveTestForStudent(student=student, test=test)
                        activated_relation.save()
                elif "group_id" in data:
                    group_id = data["group_id"]
                    group = Group.objects.get(id__exact=group_id)
                    activated_relation = ActiveTestForGroup(group=group, test=test)
                    activated_relation.save()
            elif state == "0":
                test.key = random.randint(0,15)
                test.save()
                if "students_id" in data:
                    students_id = data["students_id"]
                    print(students_id)
                    students = Student.objects.filter(id__in=students_id)
                    relations = ActiveTestForStudent.objects.filter(student__in=students)
                    relations.delete()
                elif "group_id" in data:
                    group_id = data["group_id"]
                    group = Group.objects.filter(id__exact=group_id)
                    relations = ActiveTestForGroup.objects.filter(group=group)
                    relations.delete()
            response_data = {"test_name": test.name}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        if data["method"] == "send":
            if request.user.is_authenticated():
                test_id = data["test_id"]
                received_answers = data["answers"]
                username = request.user.username
                test = Test.objects.get(id__exact=test_id)
                solved_test = SolvedTest(test=test)
                solved_test.save()
                score = 0
                for answer in received_answers:
                    answer_object = Answer.objects.get(id__exact=answer["answer_id"])
                    if answer_object.good:
                        score += 1
                solved_test.score = score
                solved_test.max = len(received_answers)
                solved_test.save()
                student = Student.objects.get(user__username=username)
                student.solved_tests.add(solved_test)
                student.save()
                # queryset = SolvedTest.objects.all()
                # serializer = SolvedTestSerializer(queryset, many=True, context={'request': request})
            return HttpResponse()
        if data["method"] == "give_me_my_grades_bitch":
            if request.user.is_authenticated():
                username = request.user.username
                student = Student.objects.get(user__username=username)
                queryset = student.solved_tests.all()
                serializer = SolvedTestSerializer(queryset, many=True, context={'request': request})
                return Response(serializer.data)
    if request.method == 'GET':
        serializer = TestSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
def questions(request):
    data = request.data # typ dict
    if request.method == 'POST':
        queryset = Question.objects.all().values('id', 'content')
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
    response_data = {'result': 'error'}
    if request.method == 'POST':
        if data["method"] == "about":
            username = request.user.username
            student_queryset = Student.objects.filter(user__username=username)
            lecturer_queryset = Lecturer.objects.filter(user__username=username)
            if student_queryset.count() > 0:
                response_data['result'] = '1'
            elif lecturer_queryset.count() > 0:
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


