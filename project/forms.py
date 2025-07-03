from django import forms
from .models import Project, Task, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



# Register Form using UserCreationForm with email field
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class AuthenticationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_pass = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        clean_data = super().clean()
        pwd = clean_data['password']
        confirm_pwd = clean_data['confirm_pass']

        if pwd != confirm_pwd:
            return forms.validationError('Password Does Not Match')
        
    class Meta():
        model = User
        fields = ['first_name', 'username', 'email', 'password']





# Register Form using UserCreationForm with email field
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

# Optional: Custom user creation form with confirmation
class MyForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_pass = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")    
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password']    


def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_pass = cleaned_data.get('confirm_pass')        
        
        if password and confirm_pass and password != confirm_pass:
            raise forms.ValidationError("Passwords do not match.")


        