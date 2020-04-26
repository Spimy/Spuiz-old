from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here
class RegistrationForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in ["username", "email", "password1", "password2"]:
            self.fields[field_name].help_text = None
    
    email = forms.EmailField(required=True, label="Email", max_length=255, widget=forms.EmailInput(attrs={'autofocus': True}))
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        
        if commit:
            user.save()
            
        return user
