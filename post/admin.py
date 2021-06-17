from django.contrib import admin
from .models import Post
from django import forms

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = '__all__'

@admin.register(Post) 
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'created_at']
    list_display_links = ['author', 'title']
    form = PostForm   #admin 페이지에서 내용 입력하는 부분

    