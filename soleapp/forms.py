from django import forms
from .models import DiarySubmission

class PartialSubmissionForm(forms.ModelForm):
    class Meta:
        model = DiarySubmission
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Divulge your deepest, darkest secrets...'}),
        }
