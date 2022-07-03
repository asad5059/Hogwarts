from turtle import title
from unicodedata import category
from django import forms
from .models import Category, Course


class CourseForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select Course Category",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'f2'})
    )
    class Meta:
        model = Course
        fields = ['title', 'category', 'short_description', 'description', 'video_url',
                  'outcome', 'requirements', 'language', 'price', 'level', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter the course title', 'id': 'f1', 'class': 'form-control'}),
            'short_description': forms.TextInput(attrs={'placeholder': 'Write a short description', 'class': 'form-control', 'id': 'f3'}),
            'outcome': forms.TextInput(attrs={'placeholder': 'write about outcome', 'class': 'form-control', 'id': 'f5'}),
            'requirements': forms.TextInput(attrs={'placeholder': 'write about requirements', 'class': 'form-control', 'id': 'f6'}),
            'language': forms.TextInput(attrs={'placeholder': 'Which Language is used for this course?', 'class': 'form-control', 'id': 'f7'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'value': '19.99', 'id': 'f8'}),
            'level': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Difficulty of this course?', 'id': 'f9'}),
            'video_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the URL of this course', 'id': 'f10'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

