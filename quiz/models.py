from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    course_name = models.CharField(max_length=40,unique=True)
    description=models.TextField()


    def __str__(self):
        return self.course_name


class SubCategory(models.Model):
    topic = models.CharField(max_length=255,unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes')
    description = models.TextField()

    def __str__(self):
        return self.topic


class Question(models.Model):
    subtopic = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    answer=models.TextField()

    def __str__(self):
        return self.question


class Exam(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE)
    score=models.IntegerField()
    date=models.DateTimeField(default=timezone.now())
    quiz_topic=models.ForeignKey(SubCategory,on_delete=models.CASCADE)

    def __str__(self):
        return self.quiz_topic.topic

class QuizResults(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    user_answer=models.CharField(max_length=200)
    student_name=models.ForeignKey(User,on_delete=models.CASCADE)
    user_topic=models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    written_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.user_answer


