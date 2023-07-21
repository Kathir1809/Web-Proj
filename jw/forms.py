from django.contrib.auth.forms import  PasswordResetForm



class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs) 

        self.fields['email'].widget.attrs.update({'class':'input', 'placeholder':'Enter your email'})

