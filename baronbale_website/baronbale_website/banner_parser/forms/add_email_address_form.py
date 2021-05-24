from django import forms


class AddEmailAddressForm(forms.Form):
    email_address = forms.EmailField()
