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

class CompletedQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="quiz", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    completed_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.quiz.title} by {self.user.username}"

    class Meta:
            verbose_name_plural = "Completed Quizzes"

class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    slug = models.SlugField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to="User_Avatars", null=True, blank=True)
    banner = models.ImageField(upload_to="User_Banners", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    following = models.ManyToManyField(User, related_name="following", blank=True)
    
    @classmethod
    def follow(cls, current_user, new_follow):
        user_profile, created = cls.objects.get_or_create(
            user=current_user
        )
        user_profile.following.add(new_follow)
    
    @classmethod
    def unfollow(cls, current_user, new_follow):
        user_profile, created = cls.objects.get_or_create(
            user=current_user
        )
        user_profile.following.remove(new_follow)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs["created"]:
        user_profile = UserProfile.objects.create(user=kwargs["instance"])
        
post_save.connect(create_profile, User)