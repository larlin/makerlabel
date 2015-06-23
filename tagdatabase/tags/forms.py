from django.forms import ModelForm
from .models import Tag
from .models import Member
from django.forms.models import inlineformset_factory

class TagForm(ModelForm):
    class Meta:
        model = Tag
        #fields = '__all__'
        exclude = ('visible', )
