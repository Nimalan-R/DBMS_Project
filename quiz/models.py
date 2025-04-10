from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.timezone import now


class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    is_student = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


def get_default_quiz():
    return Quiz.objects.first().id


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')
    created_at = models.DateTimeField(default=now)
    total_questions = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Result(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"


class ResultDetail(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='details')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.result.user.username} - Q{self.question.id} - Correct: {self.is_correct}"


class UserProgress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    total_quizzes_taken = models.PositiveIntegerField(default=0)
    total_score = models.FloatField(default=0)
    average_score = models.FloatField(default=0)
    total_time_seconds = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Progress"
