from django.forms import ModelForm, widgets
from .models import Project, Review
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # fields = '__all__'
        fields = ['title', 'description', 'featured_image','demo_link', 'source_link']

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        # fields = '__all__'
        fields = ['value', 'body']

        labels = {'value': 'Place your vote ', 'body': 'Add your comment'}

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})

        
