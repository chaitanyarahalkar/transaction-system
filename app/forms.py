from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email'}))
    address = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Address'}))
    contact = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Contact'}))
    city = forms.CharField(
        max_length=12,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'City'}))
    upi_pin = forms.CharField(
        max_length=4,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'}))

    class Meta:
        model = User
        fields = [
            'username',
            'address',
            'contact',
            'city',
            'email',
            'upi_pin',
            'password1',
            'password2']
