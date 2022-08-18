from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile


# ---------------------------------------------------------------------------- #
#                   creating a form to allow users to sign up                  #
# ---------------------------------------------------------------------------- #

# ----------------------------- USer signup form ----------------------------- #
class UserCreation(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super(UserCreation, self).save(commit=False)
        if commit:
            user.is_active = True
            user.save()

        return user
