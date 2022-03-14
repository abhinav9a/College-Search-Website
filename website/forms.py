from django.contrib.auth.forms import PasswordResetForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import EducationDetails, RATINGS, Inquiry, Review
import re

# from django.contrib.auth import get_user_model

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class RegistationForm(CustomUserCreationForm):

    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Full Name',
        }))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
        }))
    contact_number = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={
            'pattern': '^[7-9]{1}[0-9]{9}',
            'class': 'form-control',
            'placeholder': 'Mobile Number',
        }))
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        }))

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'contact_number', 'password1', 'password2']

    def clean_name(self):
        name = self.cleaned_data["name"]
        pattern = re.compile(r'[A-Za-z]{3,128}( [A-Za-z]{3,128})*')

        if len(name) < 3 or len(name) > 128:
            raise ValidationError(
                'Name should be longer than 3 characters and less than 128 characters.')
        if not re.fullmatch(pattern, name):
            raise ValidationError(
                'Name should only contain Alphabets and spaces.')

        return name

    def clean_contact_number(self):
        contact_number = self.cleaned_data["contact_number"]
        pattern = re.compile(r'^[7-9]{1}[0-9]{9}')

        user = CustomUser.objects.filter(contact_number=contact_number).exists()
        if user:
            raise ValidationError('This Mobile number already exists!')
        

        if len(contact_number) != 10:
            raise ValidationError(
                'Mobile Number should contain only 10 digits.')

        if not re.fullmatch(pattern, contact_number):
            raise ValidationError(
                'Mobile Number should start with 6,7,8 or 9.')

        return contact_number


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email or Mobile Number',
        }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }))


class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError(
                "There is no user registered with the specified email address!")
        return email


class EditProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Full Name',
        }))
    dob = forms.DateField(required=False, widget=forms.DateInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD',
        }))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
        }))
    contact_number = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={
            'pattern': '^[7-9]{1}[0-9]{9}',
            'class': 'form-control',
            'placeholder': 'Mobile Number',
        }))

    street = forms.CharField(max_length=64, required=False,  widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Street',
        }))
    country = forms.CharField(max_length=64, required=False,  widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Country',
        }))
    state = forms.CharField(max_length=64, required=False,  widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'State',
        }))
    city = forms.CharField(max_length=64, required=False,  widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'City',
        }))
    pincode = forms.CharField(max_length=6, required=False,  widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Pincode',
        }))

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'dob', 'contact_number',
                  'street', 'city', 'state', 'country', 'pincode']
        required = ('name', 'email', 'contact_number')


class EducationalDetailsForm(forms.ModelForm):
    class Meta:
        model = EducationDetails
        exclude = ('user',)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('user', 'college')
        # fields = '__all__'

        widgets = {
            'ratings': forms.Select(attrs={'class': 'form-control',  'choices': RATINGS}),
            'comment': forms.Textarea(attrs={'class': 'form-control', })
        }


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        exclude = ('is_solved',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', }),
            'email': forms.EmailInput(attrs={'class': 'form-control', }),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'pattern': '^[7-9]{1}[0-9]{9}'}),
            'message': forms.Textarea(attrs={'class': 'form-control', }),
        }

    def clean_contact_number(self):
        contact_number = self.cleaned_data["contact_number"]
        pattern = re.compile(r'^[7-9]{1}[0-9]{9}')

        if len(contact_number) != 10:
            raise ValidationError(
                'Mobile Number should contain 10 digits.')

        if not contact_number.isdigit():
            raise ValidationError(
                'Mobile Number should only contain numbers.')

        if not re.fullmatch(pattern, contact_number):
            raise ValidationError(
                'Mobile Number should start with 6,7,8 or 9.')

        return contact_number
