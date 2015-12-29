
from django.db import models


class Lecturer(models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=64)

    def __str__(self):
        return '%s' % (self.login)


class Student(models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=64)

    def __str__(self):
        return '%d %s' % (self.id, self.login)


class Group(models.Model):
    name = models.CharField(max_length=50, default='grupa')
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return '%s, %s' % (self.lecturer, self.name)


class Question(models.Model):
    TYPES = ((0, 'zamkniete'), (1, 'otwarte'))

    content = models.TextField()
    type = models.IntegerField(choices=TYPES, default=0)

    def __str__(self):
        return '%s / %s' % (self.content, self.TYPES[self.type][1])


class Answer(models.Model):
    content = models.CharField(max_length=120, default='treść odpowiedzi')
    good = models.BooleanField(default=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return '%s | %s | %r' % (self.question, self.content, self.good)


class Test(models.Model):
    state = models.IntegerField(default=0)
    key = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    questions = models.ManyToManyField(Question)
