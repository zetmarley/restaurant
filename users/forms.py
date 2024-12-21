from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import HiddenInput

from users.models import User


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'job_title', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = HiddenInput()