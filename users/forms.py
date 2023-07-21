from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import Profiles, Skills, Message


class CustomUserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','email','username','password1','password2']
        labels = {
            'first_name':'Name'
        }


    def __init__(self, *args, **kwargs):
        super(CustomUserCreation, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class':'input input--text', 'placeholder':'Add Name'})
        self.fields['email'].widget.attrs.update({'class':'input input--email', 'placeholder':'Add Email'})
        self.fields['username'].widget.attrs.update({'class':'input input--text', 'placeholder':'Add Username'})
        self.fields['password1'].widget.attrs.update({'class':'input input--password', 'placeholder':'Add Password'})
        self.fields['password2'].widget.attrs.update({'class':'input input--password', 'placeholder':'Confirm Password'})



class ProfileEdit(ModelForm):
    class Meta:
        model = Profiles
        fields = ['name', 'email', 'username', 'location', 'bio', 'short_intro', 'profile_image',
                  'social_github', 'social_linkedin', 'social_youtube', 'social_website', 'social_twitter']
        
    
    def __init__(self, *args, **kwargs):
        super(ProfileEdit, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})



class skillsAdd(ModelForm):
    class Meta:
        model = Skills
        fields = ['name', 'description']

    
    def __init__(self, *args, **kwargs):
        super(skillsAdd, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class':'input', 'placeholder':'Add Name'})
        self.fields['description'].widget.attrs.update({'class':'input', 'placeholder':'Add Description'})




class sendMessage(ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']


    def __init__(self, *args, **kwargs):
        super(sendMessage, self).__init__(*args, **kwargs)

        self.fields['subject'].widget.attrs.update({'class':'input', 'placeholder':'Add Subject'})
        self.fields['body'].widget.attrs.update({'class':'input', 'placeholder':'Add Body of the message'})


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class':'input', 'placeholder':'Enter your email'})

    