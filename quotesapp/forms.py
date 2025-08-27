from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .views import Quote, Source


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }


class QuoteForm(forms.ModelForm):
    source_category = forms.CharField(max_length=255, label="Категория источника")
    source_name = forms.CharField(max_length=255, label="Название источника")
    weight = forms.IntegerField(
        label="Вес цитаты",
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={'type': 'range', 'class': 'form-range'})
    )

    class Meta:
        model = Quote
        fields = ['text', 'weight']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        category = cleaned_data.get("source_category")
        name = cleaned_data.get("source_name")

        source, created = Source.objects.get_or_create(category=category, name=name)

        if Quote.objects.filter(source=source, text=text).exists():
            raise forms.ValidationError("Такая цитата уже существует для этого источника.")

        if Quote.objects.filter(source=source).count() >= 3:
            raise forms.ValidationError("У этого источника уже есть 3 цитаты.")

        self.cleaned_data['source_instance'] = source

        return cleaned_data

