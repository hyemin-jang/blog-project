from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.contrib.auth import get_user_model #장고 내부 User모델을 잡음
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def post_list(request): 
    posts = Post.objects.all()    
    
    #여기서 request는?? post 폼의 title / content / photo
    if request.user.is_authenticated: #사용자가 로그인 상태일때
        nickname = request.user #사용자 이메일계정 저장
        user = get_object_or_404(get_user_model(), nickname=nickname)
        #get_objedt_or_404 : 첫번째인자=모델, 두번째인자=그 모델 클래스에서 어떤객체인지 / 없으면 404반환
        user_profile = user #사용자의 프로필 저장
        
        if request.method == "POST":        
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False) #commit=False : 데이터베이스에 바로 저장되지 않도록 함(유저 정보를 넣은 후 저장할것임)
                post.author = request.user
                post.save()
                messages.success(request, '새 글이 등록되었습니다.')
                return redirect('/')
        else:
            form= PostForm()

    
        return render(request, 'post/post_list.html', {
            'user_profile': user_profile,
            'posts': posts,   
            'form': form,        
        })
    else:
        return render(request, 'post/post_list.html', {            
            'posts': posts,                   
        })
    