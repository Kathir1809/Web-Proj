from django.forms import ModelForm
from .models import Project, Tag, Review
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','featured_image', 'description', 'demo_link', 'source_link']

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({'class':'input', 'placeholder':'Add title'})
        self.fields['featured_image'].widget.attrs.update({'class':'input'})
        self.fields['description'].widget.attrs.update({'class':'input', 'placeholder':'Add description'})
        self.fields['demo_link'].widget.attrs.update({'class':'input', 'placeholder':'Add Demo link'})
        self.fields['source_link'].widget.attrs.update({'class':'input', 'placeholder':'Add Source link'})
        # self.fields['tags'].widget.attrs.update({'class':'input'})


class AddTag(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(AddTag, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class':'input', 'placeholder':'Add Tag name'})

class Reviewform(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']

    labels = {
        'value' : 'Place your vote',
        'body' : 'Add a comment with your Vote'
    }

    def __init__(self, *args, **kwargs):
        super(Reviewform, self).__init__(*args, **kwargs)

        self.fields['value'].widget.attrs.update({'class':'input'})
        self.fields['body'].widget.attrs.update({'class':'input', 'placeholder':'Add a comment'})

    
