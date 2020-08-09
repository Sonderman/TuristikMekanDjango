from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput, ModelForm

from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')  # "__all__"
        widgets = {
            'Kullanıcı Adı': TextInput(attrs={'class': 'input', 'placeholder': 'Kullanıcı Adı'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'email'}),
            'İsim': TextInput(attrs={'class': 'input', 'placeholder': 'İsim'}),
            'Soyisim': TextInput(attrs={'class': 'input', 'placeholder': 'Soyisim'})
        }


CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
]


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country', 'image']
        widgets = {
            'Tel No': TextInput(attrs={'class': 'input', 'placeholder': 'Tel No'}),
            'Adres': TextInput(attrs={'class': 'input', 'placeholder': 'Adres'}),
            'Şehir': Select(attrs={'class': 'input', 'placeholder': 'Şehir'}, choices=CITY),
            'Ülke': TextInput(attrs={'class': 'input', 'placeholder': 'Ülke'}),
            'Profil Resimi': FileInput(attrs={'class': 'input', 'placeholder': 'Profil Resimi'})
        }
