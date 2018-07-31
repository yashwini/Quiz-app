from django import forms
from quiz.models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        exclude=['id']
        widgets={
            'course_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Category'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),
        }

class SubCategoryForm(forms.ModelForm):
    category=forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={ 'class': 'form-control'}),empty_label='Select Course')
    class Meta:
        model=SubCategory
        exclude=['id']
        widgets={
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter topic'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Description'}),
        }

class QuestionsForm(forms.ModelForm):
    subtopic=forms.ModelChoiceField(queryset=SubCategory.objects.all(),widget=forms.Select(attrs={ 'class': 'form-control'}),empty_label='Select Topic')
    class Meta:
        model=Question
        exclude=['id']
        widgets={
            'subtopic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subtopic'}),
            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Full Question'}),
            'option1':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Option 1'}),
            'option2':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Option 2'}),
            'option3':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Option 3'}),
            'option4':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Option 4'}),
            'answer':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' answer'})
        }

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name '}))

    email = forms.EmailField(max_length=50,required=True,
                                 widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email id '}))

    username = forms.CharField(max_length=20,required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))


    password = forms.CharField(max_length=15,required=True,
                                 widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password '}))




class LoginForm(forms.Form):
    username = forms.CharField(max_length=20,required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))


    password = forms.CharField(max_length=15,required=True,
                                 widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password '}))
