from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import datetime


#BaseUserManager: User를 생성할때 사용하는 헬퍼 클래스. 
#모든 장고 모델들은 Manager를 통해서 QuerySet을 받음. DB에서 쿼리를 처리할 때 Manager를 무조건 거쳐야함


class UserManager(BaseUserManager):    
    
    use_in_migrations = True    #???
    
    # Helper 클래스인 class UserManager(BaseUserManager)의 두가지 메서드 제공: create_user, create_superuser
    # create_user(*username_filed*, password=None, **other_fields)
    # 첫번째 ㅏ라미터가 username인데 나는 대신 email을 쓸것

    def create_user(self, email, nickname, password=None):        
        if not email :            
            raise ValueError('Users must have an email address.')
              
        user = self.model(            
            email = self.normalize_email(email),            
            nickname = nickname        
        )        
        user.set_password(password)        
        user.save(using=self._db)        
        return user     

    def create_superuser(self, email, nickname, password):        
        user = self.create_user(            
            email = self.normalize_email(email),       
            nickname = nickname,            
            password=password        
        )        
        user.is_superuser = True  
        user.is_admin = True
        user.save(using=self._db)        
        return user 

# 실제 모델
class Profile(AbstractBaseUser,PermissionsMixin):    
    
    #AbstractBaseUser는 password, last_login, is_active 필드만 제공

    objects = UserManager() #objects: 헬퍼 클래스 지정

    def user_picture_path(instance, filename):
        now= datetime.datetime.now()
        return 'accounts/{}/{}.jpg'.format(instance.nickname, now.strftime('%Y/%m/%d'))
    
    email = models.EmailField(max_length=255, unique=True, default="")   
    
    nickname = models.CharField(max_length=20, unique=True, default="")
    picture = ProcessedImageField(upload_to= user_picture_path, 
                                processors=[ResizeToFill(150,150)],
                                format='JPEG', options={'quality':90},
                                blank=True)
    date_joined = models.DateTimeField(auto_now_add=True) 
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)
                            
    
    USERNAME_FIELD = 'email'    #나는 이메일로 할것임
    REQUIRED_FIELDS = ['nickname']   

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
        
    @property
    def is_staff(self):
        return self.is_admin