from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
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
    score = models.IntegerField()
    completed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quiz.title} by {self.user.username}"

    class Meta:
            verbose_name_plural = "Completed Quizzes"

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    read = models.BooleanField(default=False)
    for_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="for_user", null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user", null=True)
    
    def __str__(self):
        return f"\"{self.title}\" notification for {self.for_user.username}"
    
class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    slug = models.SlugField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to="User_Avatars", null=True, blank=True)
    banner = models.ImageField(upload_to="User_Banners", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    following = models.ManyToManyField(User, related_name="following", blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs.get("created", False):
        user_profile = UserProfile.objects.create(user=kwargs["instance"])
        
def noticiations_manager(boolean, author, title, message):
    if boolean:
        user_profiles = UserProfile.objects.all()
        
        for user_profile in user_profiles:
            
            if user_profile.user == author: 
                continue
            
            if author in user_profile.following.all():
                Notification.objects.create(title=title,
                                            message=message,
                                            for_user=user_profile.user,
                                            from_user=author)
    
def create_quiz(sender, instance, **kwargs):
    noticiations_manager(kwargs.get("created", False),
                          instance.author,
                          "New Quiz",
                          f"{instance.author.username} has created a new quiz titled \"{instance.title}\"!")

def delete_quiz(sender, instance, **kwargs):
    noticiations_manager(True,
                          instance.author,
                          "Deleted Quiz",
                          f"{instance.author.username} has delete a quiz titled \"{instance.title}\"!")

def complete_quiz(sender, instance, **kwargs):
    noticiations_manager(kwargs.get("created", False),
                          instance.user,
                          "Completed Quiz",
                          f"{instance.user.username} has completed a quiz titled \"{instance.quiz.title}\"!")

post_save.connect(create_profile, User)

post_save.connect(create_quiz, Quiz)
post_delete.connect(delete_quiz, Quiz)

post_save.connect(complete_quiz, CompletedQuiz)
