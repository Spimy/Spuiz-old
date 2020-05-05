from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField


# Create your models here.

class CorrectAnswer(models.Model):
    answer = models.CharField(max_length=255)
    
    def __str__(self):
        return self.answer
    
class WrongAnswer(models.Model):
    answer = models.CharField(max_length=255)
    
    def __str__(self):
        return self.answer

class Question(models.Model):
    
    question = models.CharField(max_length=255)
    correct = models.ManyToManyField(CorrectAnswer)
    wrong = models.ManyToManyField(WrongAnswer, blank=True)
    thumbnail = models.ImageField(upload_to="Question_Thumbnails", blank=True, null=True)
    
    def __str__(self):
        return self.question
    
class Quiz(models.Model):
    
    slug = models.SlugField(max_length=255, blank=True, null=True)
    
    thumbnail = models.ImageField(upload_to="Quiz_Thumbnails")
    title = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question)
    
    media_quiz = models.BooleanField(default=False)
    mcq = models.BooleanField(default=False)
    
    upvotes = models.ManyToManyField(User, blank=True, related_name="upvotes")
    downvotes = models.ManyToManyField(User, blank=True, related_name="downvotes")
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Quiz, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Quizzes"
    
class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    slug = models.SlugField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to="User_Avatars", null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs["created"]:
        user_profile = UserProfile.objects.create(user=kwargs["instance"])
        
post_save.connect(create_profile, User)