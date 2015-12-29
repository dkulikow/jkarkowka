from django.db import models


class Lecturer(models.Model):
    name = models.CharField(max_length=50, default='Imie')
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=64)

    def __str__(self):
        return '%s' % (self.login)


class Answer(models.Model):
    content = models.CharField(max_length=120, default='treść odpowiedzi')
    good = models.BooleanField(default=True)

    def __str__(self):
        return ' %s | %r' % (self.content, self.good)


class Question(models.Model):
    TYPES = ((0, 'zamkniete'), (1, 'otwarte'))
    content = models.TextField()
    type = models.IntegerField(choices=TYPES, default=0)
    answers = models.ManyToManyField(Answer)

    def __str__(self):
        return '%s / %s' % (self.content, self.TYPES[self.type][1])


class Test(models.Model):
    state = models.IntegerField(default=0)
    key = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    questions = models.ManyToManyField(Question)


class SolvedTest(models.Model):
    test = models.ForeignKey(Test)
    answers = models.ManyToManyField(Answer)


class Student(models.Model):
    name = models.CharField(max_length=50, default='Imie')
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=64)
    solved_test = models.ManyToManyField(SolvedTest)

    def __str__(self):
        return '%d %s' % (self.id, self.login)


class Group(models.Model):
    name = models.CharField(max_length=50, default='grupa', unique=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return '%s, %s' % (self.lecturer, self.name)


class StudentSession(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    authToken = models.CharField(max_length=64)
    refreshToken = models.CharField(max_length=64)
    expireDate = models.DateTimeField()


class LecturerSession(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    authToken = models.CharField(max_length=64)
    refreshToken = models.CharField(max_length=64)
    expireDate = models.DateTimeField()
