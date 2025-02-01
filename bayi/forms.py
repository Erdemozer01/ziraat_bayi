from django import forms
from accounts.models import Customer
from django.contrib.auth.models import User

from bayi.models import Contact


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class CustomerForm(forms.ModelForm):
    last_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Son ödeme tarihi',
                                help_text='Şimdi ödeyecekseniz boş bırakın', required=False)

    valid = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'type': 'checkbox'}),
                               label='Bilgilerimin doğruluğunu kontrol ettim ve satın alma işlemini onalıyorum.')

    payment = forms.ChoiceField(
        label='Ödeme yöntemi seçiniz',
        required=True,
        choices={'': '-----', 'Nakit': 'Nakit', 'Kredi Kartı': 'Kredi Kartı', 'Borç': 'Borç'},
    )

    class Meta:
        model = Customer

        fields = ['address', 'telephone', 'payment', 'last_date', 'valid']

        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }

    def clean(self):
        if self.cleaned_data['payment'] == 'Borç':
            if self.cleaned_data['last_date'] is None:
                self.add_error(field='last_date', error='Borç işaretlediğiniz için son ödeme tarihini giriniz')
        return self.cleaned_data


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
        fields = ('subject', 'name', 'email', 'message')
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
