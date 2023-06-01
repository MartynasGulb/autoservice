from .models import OrderComment, Profile, Order
from django import forms
from django.contrib.auth.models import User


class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = OrderComment
        fields = ["content"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class MyDateTimeInput(forms.DateInput):
    input_type = 'datetime-local'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['vehicle', 'deadline', 'status']
        widgets = {'deadline': MyDateTimeInput()}
