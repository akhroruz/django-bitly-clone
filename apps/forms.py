from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, PasswordInput

from apps.models import Url, User


class UrlForm(ModelForm):
    class Meta:
        model = Url
        exclude = ('short_name',)


class CustomCreateUserForm(ModelForm):
    confirm_password = CharField(widget=PasswordInput(attrs={"autocomplete": "current-password"}), )

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if confirm_password != password:
            raise ValidationError('Parolni tekshiring!')
        return make_password(password)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password')


class CustomLoginForm(AuthenticationForm):
    def clean_password(self):
        username = self.data.get('username')
        password = self.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and not user.check_password(password):
            raise ValidationError('The password or username did not match')
        return password

