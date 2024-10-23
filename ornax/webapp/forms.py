from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import TextInput, PasswordInput
from .models import Product
    
# --Registering a User
class UserRegistration(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","password1","password2"]

# --User Login
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# --ProductEntry
class ProductEntryForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product_id","product_name","product_brand","product_mfg_year","product_image_url","product_url","product_stock","product_price","product_description"]


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product_id","product_name","product_brand","product_mfg_year","product_image_url","product_url","product_stock","product_price","product_description"]


    
