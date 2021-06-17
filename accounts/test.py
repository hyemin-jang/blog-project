from .models import Profile

user = Profile.objects.create_user('email', 'password','nickname')
user.save()
print(user)