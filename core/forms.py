from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Your message here...'
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@rcciit.org.in'):  # Domain validation
            raise forms.ValidationError("Please use your RCCIIT email.")
        return email