from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


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
        return '%s ' % (self.content)


class Test(models.Model):
    state = models.IntegerField(default=0)
    key = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return '%s' % (self.name)


class SolvedTest(models.Model):
    test = models.ForeignKey(Test)
    answers = models.ManyToManyField(Answer)

    def __str__(self):
        return '%s, %s' % (self.test, self.answers)

    def __unicode__(self):
        return '%s, %s' % (self.test, self.answers)


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    solved_tests = models.ManyToManyField(SolvedTest)

    def __str__(self):
        return '%d, %s' % (self.id, self.user)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = Student.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Group(models.Model):
    name = models.CharField(max_length=50, default='grupa', unique=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
    activated_tests = models.ManyToManyField(Test)

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
