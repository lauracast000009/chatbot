from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    grade = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.grade}"

class Exercise(models.Model):
    TYPE_CHOICES = [
        ('single', 'Single choice'),
        ('multiple', 'Multiple choice'),
        ('open', 'Open answer'),
    ]
    title = models.CharField(max_length=255)
    question = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='single')
    level = models.IntegerField(default=1)
    correct_answer = models.TextField(blank=True)
    metadata = models.JSONField(blank=True, null=True)  # opciones, etc.
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_exercises')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ExerciseResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    score = models.FloatField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.exercise.title} - {self.score}"

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} - {self.user.username}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=50)  # 'student' or 'bot' or username
    text = models.TextField()
    bot_response = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text[:30]}"
