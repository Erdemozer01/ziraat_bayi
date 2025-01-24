from django import forms
from accounts.models import Customer
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',  'email']



class CustomerForm(forms.ModelForm):

    class Meta:

        model = Customer

        fields = ['address', 'telephone']

        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }




