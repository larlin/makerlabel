from django.forms import ModelForm
from django import forms
from .models import Tag
from .models import Member
from django.forms.models import inlineformset_factory
from django.utils import timezone
from django.core.exceptions import ValidationError

class TagForm(ModelForm):
    # extra fields from Member...
    name = forms.CharField(max_length=20, required=False)
    member_number = forms.IntegerField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        
        self.fields['member_id'].required = False
        self.fields['member_id'].blank = True
        self.fields['member_id'].null = True
        
    
    class Meta:
        model = Tag
        #fields = '__all__'
        exclude = ('print_date', 'box_number', 'visible', )
    
    def clean(self):
        cleaned_data = super(TagForm, self).clean()
        member = cleaned_data.get("member_id")
        name = cleaned_data.get("name")
        member_number = cleaned_data.get("member_number")
        
        # If we don't have a member_id try to clean name and member_number
        if member is None:
            member = Member(name=name, member_number=member_number, box_num = 0)
            print("Trying to clean:")
            try:
                member.full_clean()
            except ValidationError as e:
                print("raising valiation error")
                msg = "Failed to create member, either select a old member or add data to create a new."
                self.add_error('name', msg)
                self.add_error('member_id', msg)
            print("Member:")
            print(member.__dict__)
            # TODO: This is ugly and bad, setting id to trick the verfication
            # of user in the case that member id is not set because we are
            # creating a new member now. This is really bad as it requires
            # user id 1 to be in use at all times. There must be a way to handle
            # this situation without saving the user before save(commit=True) is
            # called.
            member.id = 1
            member.new_member = True
            print(self.cleaned_data)
            self.cleaned_data['member_id'] = member
            print(self.cleaned_data)
        else:
            member.new_member = False
        
        return cleaned_data
        
    def save(self, commit=True):
        print("After save")
        tag = super(TagForm, self).save(commit=False)
        tag.print_date = timezone.now()
        tag.box_number = self.cleaned_data['member_id'].box_num
        if self.cleaned_data['member_id'].new_member :
            self.cleaned_data['member_id'].id = None
        if commit:
            self.cleaned_data['member_id'].box_num = self.cleaned_data['member_id'].box_num + 1
            self.cleaned_data['member_id'].save()
        tag.member_id = self.cleaned_data['member_id']
        print(self.cleaned_data)
        return super(TagForm, self).save(commit=commit)

