# commerce/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model  # Get the custom user model dynamically
from .models import Profile  # Import the Profile model

# Use the custom user model dynamically
CustomUser = get_user_model()

# Custom SignUpForm for user registration
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        # Use the custom user model defined in settings.py
        model = CustomUser  # Correct reference to custom user model
        fields = ['username', 'email', 'password1', 'password2']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None  # Remove help texts
            field.error_messages = {'required': 'This field is required.'}  # Customize error messages


# ProfileForm for updating user profile information
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile  # Reference the Profile model correctly
        fields = ['bio', 'location', 'birth_date', 'image']  # Fields displayed in the form


# ProfileUpdateForm for updating user profile data
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile  # Correctly reference the Profile model class
        fields = ['image', 'bio', 'location', 'birth_date']  # Fields user can update



# commerce/forms.py

from django import forms
from .models import ContactMessage

# forms.py

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 5}),
        }


# forms.py
from django import forms

class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16)
    expiry_date = forms.CharField(max_length=5)  # MM/YY
    cvv = forms.CharField(max_length=3)
