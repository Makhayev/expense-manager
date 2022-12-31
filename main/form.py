from .models import Task
from django.forms import ModelForm, TextInput, Select, DateInput
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"
        
        
    class Meta:
        model = Task
        fields = ['money', 'category', 'budget', 'description', 'date']
        widgets = {
            'money': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сумма',
                'type': 'number',
                }),
            'category': Select(attrs={
                'class': 'form-select',
                'placeholder': 'Категория'
                }),
            'budget': Select(attrs={
                'class': 'form-select',
                'placeholder': 'Бюджет'
                }),
            'date': DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                }),
            'description': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Описание',
                }),
        }

class AuthForm(AuthenticationForm, ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].widget.attrs['class'] = 'form-control mb-4'
            self.fields[fieldname].help_text = None
            self.fields[fieldname].label = ''
        for fieldname in ['username']:
                self.fields[fieldname].widget.attrs['placeholder'] = 'Логин'
        for fieldname in ['password']:
                self.fields[fieldname].widget.attrs['placeholder'] = 'Пароль'

class RegForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control mb-4',
                'placeholder': 'Логин'
                }),
            'password': TextInput(attrs={
                'class': 'form-control mb-4',
                'placeholder': 'Пароль',
                'type': 'password'
                }),
        }
    def save(self, commit= True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    def __init__(self, *args, **kwargs):
            super(RegForm, self).__init__(*args, **kwargs)
            for fieldname in self.fields:
                self.fields[fieldname].help_text = None
                self.fields[fieldname].label = ''