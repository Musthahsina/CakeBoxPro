from django import forms
from cakebox.models import User,Category,Cakes,CakeVarients,Offers
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2","phone","address"]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model=Category
        fields="__all__"

class CakeAddForm(forms.ModelForm):
    class Meta:
        model=Cakes
        fields="__all__"


class CakeVarientForm(forms.ModelForm):
    class Meta:
        model=CakeVarients
        exclude=("cake",)


class CakeOfferForm(forms.ModelForm):
    class Meta:
        model=Offers
        exclude=("Cake_variant",)
        widgets={
            "start_date":forms.DateInput(attrs={"type":"date"}),
            "due_date":forms.DateInput(attrs={"type":"date"})
        }