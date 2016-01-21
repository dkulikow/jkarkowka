import random
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='Name')

    def __str__(self):
        return '%d, %s' % (self.id, self.user)


class Answer(models.Model):
    content = models.CharField(max_length=120, default='Answer')
    good = models.BooleanField(default=True)

    def __str__(self):
        return ' %s | %r' % (self.content, self.good)


class Question(models.Model):
    content = models.TextField()
    answers = models.ManyToManyField(Answer)

    def __str__(self):
        return '%s' % (self.content,)


class Test(models.Model):
    name = models.CharField(max_length=64)
    key = models.IntegerField(default=random.randint(0, 15), validators=[
        MaxValueValidator(15),
        MinValueValidator(0)
    ])
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return '%s' % (self.name,)


class SubmittedAnswer(models.Model):
    answer = models.CharField(max_length=64)


class SolvedTest(models.Model):
    test = models.ForeignKey(Test)
    score = models.IntegerField(default=0, blank=True, editable=False)
    max = models.IntegerField(default=0, blank=True, editable=False)

    def __str__(self):
        return '%s' % (self.test,)

    def __unicode__(self):
        return '%s' % (self.test,)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    solved_tests = models.ManyToManyField(SolvedTest, blank=True)

    def __str__(self):
        return '%d, %s' % (self.id, self.user)


class Group(models.Model):
    name = models.CharField(max_length=50, default='Group', unique=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return '%s, %s' % (self.lecturer, self.name)


class ActiveTestForGroup(models.Model):
    group = models.ForeignKey(Group)
    test = models.ForeignKey(Test)

    def __str__(self):
        return '%s, %s' % (self.group.name, self.test.id)


class ActiveTestForStudent(models.Model):
    student = models.ForeignKey(Student)
    test = models.ForeignKey(Test)

    def __str__(self):
        return '%s, %s' % (self.student.name, self.test.id)
