from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'job_title']

class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'job_title']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.fields['password'].widget = forms.HiddenInput()