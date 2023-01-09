from .models import Poll,Choice
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
    def __init__(self,*args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})
class PollAddForm(forms.ModelForm):
    choice1 = forms.CharField(label='Choice 1', max_length=100, min_length=1,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    choice2 = forms.CharField(label='Choice 2', max_length=100, min_length=1,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    choice3 = forms.CharField(label='Choice 3', max_length=100, min_length=1,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    choice4 = forms.CharField(label='Choice 4', max_length=100, min_length=1,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Poll
        fields = ['text', 'choice1', 'choice2','choice3','choice4']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }

class ChoiceAddForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_value', ]
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control', })
        }