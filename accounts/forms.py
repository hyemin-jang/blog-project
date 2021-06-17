from django import forms
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import Profile



class SignupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'password', 'password2', 'nickname', 'picture']

    email = forms.CharField(max_length=255, label='이메일 계정')    
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)
    nickname = forms.CharField(max_length=20, label='닉네임')
    picture = forms.ImageField(label='프로필 사진', required=False)
   

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Profile.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 존재하는 이메일입니다.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return password

    def clean_nickname(self):
        nickname= self.cleaned_data.get('nickname')
        #cleaned_data: 폼을 통해 검증에 통과된 값이 dictionary타입으로 제공됨
        if Profile.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError('이미 존재하는 닉네임입니다.')
        return nickname

    def clean_picture(self):
        picture= self.cleaned_data.get('picture')
        if not picture:
            picture=None
        return picture

    def save(self):
        new_user = Profile.objects.create_user(  #create_user를 써야 set_password를 통해 비밀번호 해쉬화됨
                email= self.cleaned_data['email'],
                password = self.cleaned_data['password'],
                nickname = self.cleaned_data['nickname']
            )
        new_user.picture = self.cleaned_data['picture']
        new_user.save()

        

class LoginForm(AuthenticationForm):
    username= forms.CharField(max_length=255, label="이메일 계정")
    password= forms.CharField(label="비밀번호", widget=forms.PasswordInput)
    
    error_messages = {
        'invalid_login': ("이메일이나 비밀번호가 올바르지 않습니다."),
        'inactive': ("이 계정은 인증되지 않았습니다.")
    }