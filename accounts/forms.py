from django import forms
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import Profile



class SignupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'password', 'password2', 'nickname', 'picture']
        
    email = forms.CharField(max_length=255, widget=forms.EmailInput(attrs={
        'class': 'form_input',
        'placeholder': '이메일'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form_input',
        'placeholder': '비밀번호',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form_input',
        'placeholder': '비밀번호 확인'
    }))
    nickname = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'form_input',
        'placeholder': '닉네임'
    }))
    picture = forms.ImageField(required=False)
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Profile.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 존재하는 이메일입니다.')
        return email

    def clean_password2(self):
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

  

    def save(self):  #폼에서 유효성검사 통과한 데이터들을 저장할것임
        Profile.objects.create(
            nickname=self.cleaned_data['nickname'],
            password=self.cleaned_data['password2'],
            email=self.cleaned_data['email'],
            picture=self.cleaned_data['picture'],
        )
        return 

class LoginForm(AuthenticationForm):
    username= forms.CharField(max_length=255, widget=forms.EmailInput(attrs={
        'class': 'form_input',
        'placeholder': '이메일'
    }))
    password= forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form_input',
        'placeholder': '비밀번호'
    }))
    
    error_messages = {
        'invalid_login': ("이메일이나 비밀번호가 올바르지 않습니다."),
        'inactive': ("이 계정은 인증되지 않았습니다.")
    }