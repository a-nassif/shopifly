# store_admin/forms.py
from django import forms
from store.models import Store, Theme

# store_admin/forms.py
from django import forms
from .models import StoreOwnerUser
from .models import Store


class StoreOwnerRegistrationForm(forms.Form):
    store_name = forms.CharField(max_length=255)
    subdomain = forms.SlugField(max_length=100)
    email = forms.EmailField()
    name = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_subdomain(self):
        subdomain = self.cleaned_data['subdomain']
        if Store.objects.filter(subdomain=subdomain).exists():
            raise forms.ValidationError("Subdomain is already taken.")
        return subdomain

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get("password")
        cpw = cleaned_data.get("confirm_password")
        if pw and cpw and pw != cpw:
            self.add_error("confirm_password", "Passwords do not match.")


class StoreSettingsForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'subdomain', 'custom_domain', 'logo', 'theme',
                  'brand_color', 'currency']
        widgets = {
            'brand_color': forms.TextInput(attrs={'type': 'color'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['theme'].queryset = Theme.objects.all()
        self.fields['theme'].empty_label = "Choose a theme"
        self.fields['theme'].widget.attrs.update({'class': 'form-select'})
