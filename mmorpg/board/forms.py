from django.forms import ModelForm
from .models import Post, Response
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', "text" , 'category','postUser']

class ResponseForm(ModelForm):
    class Meta:
        model = Response
        # fields = [ 'responsePost','responseUser', "text" ]
        fields = ["text",]