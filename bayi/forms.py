from django import forms
from accounts.models import Customer
from django.contrib.auth.models import User

from bayi.models import Product, Contact


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class CustomerForm(forms.ModelForm):
    last_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Son ödeme tarihi',
                                help_text='Şimdi ödeyecekseniz boş bırakın', required=False)

    valid = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'type': 'checkbox'}),
                               label='Bilgilerimin doğruluğunu kontrol ettim ve satın alma işlemini onalıyorum.')

    class Meta:
        model = Customer

        fields = ['address', 'telephone', 'last_date', 'valid']

        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CustomerInformationModelForm(forms.ModelForm):
    class Meta:
        model = Customer

        fields = ['telephone', 'address', ]

        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'subject', 'message', 'email', )
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }