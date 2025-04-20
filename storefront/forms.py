from django import forms
from .models import StoreCustomerUser


class StoreCustomerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = StoreCustomerUser
        fields = ['name', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get("password")
        cpw = cleaned_data.get("confirm_password")
        if pw and cpw and pw != cpw:
            self.add_error("confirm_password", "Passwords do not match.")

        if cleaned_data.get('email') and StoreCustomerUser.objects.filter(email=cleaned_data.get('email')).exists():
            self.add_error('email', 'Email is already taken.')
