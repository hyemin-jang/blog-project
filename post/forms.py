from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'class': 'new_title'        
    }))
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'new_content'        
    }))
    photo = forms.ImageField(label='', required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'photo']