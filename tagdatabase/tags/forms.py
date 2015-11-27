from django.forms import ModelForm
from django import forms
from .models import MemberBoxTag
from .models import MachineTag
from .models import Member
from django.forms.models import inlineformset_factory
from django.utils import timezone
from django.core.exceptions import ValidationError

class AddForeginMember(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddForeginMember, self).__init__(*args, **kwargs)
        
        initial = kwargs.get('initial', {})
        if not self.member_fk in initial:
            # extra fields from Member...
            self.fields['member_name'] = forms.CharField(max_length=20, required=False)
            self.fields['member_number'] = forms.IntegerField(required=False)
        
        self.fields[self.member_fk].required = False
        self.fields[self.member_fk].blank = True
        self.fields[self.member_fk].null = True

    def clean(self):
        cleaned_data = super(AddForeginMember, self).clean()
        print(cleaned_data)
        member = cleaned_data.get(self.member_fk)
        name = cleaned_data.get("member_name")
        member_number = cleaned_data.get("member_number")
        
        # If we don't have a member_id try to clean name and member_number
        if member is None:
            member = Member(name=name, member_number=member_number, box_num = 0)
            print("Trying to clean:")
            try:
                member.full_clean()
            except ValidationError as e:
                print(member.__dict__)
                print("raising valiation error"+'; '.join(e.messages))
                msg = "Failed to create member, either select a old member or add data to create a new."
                self.add_error('member_name', msg)
                self.add_error(self.member_fk, msg)
            #print("Member:")
            #print(member.__dict__)
            # TODO: This is ugly and bad, setting id to trick the verfication
            # of user in the case that member id is not set because we are
            # creating a new member now. This is really bad as it requires
            # user id 1 to be in use at all times. There must be a way to handle
            # this situation without saving the user before save(commit=True) is
            # called.
            member.id = 1
            member.new_member = True
            print(self.cleaned_data)
            self.cleaned_data[self.member_fk] = member
            print(self.cleaned_data)
        else:
            member.new_member = False
        
        return cleaned_data
    
    def save(self, commit=True):
        print("After save")
        foreign_member_object = super(AddForeginMember, self).save(commit=False)
        if self.cleaned_data[self.member_fk].new_member : 
            self.cleaned_data[self.member_fk].id = None
        if commit:
            self.cleaned_data[self.member_fk].save()
        foreign_member_object.member_id = self.cleaned_data[self.member_fk]
        
        return super(AddForeginMember, self).save(commit=commit)
        
class MemberBoxTagForm(AddForeginMember):
    member_fk = "member_id"
    
    class Meta:
        model = MemberBoxTag
        exclude = ('print_date', 'box_number', 'visible', )
    
    def save(self, commit=True):
        tag = super(MemberBoxTagForm, self).save(commit=False)
        tag.print_date = timezone.now()
        tag.box_number = self.cleaned_data['member_id'].box_num
        if commit:
            self.cleaned_data['member_id'].box_num = self.cleaned_data['member_id'].box_num + 1
        return super(MemberBoxTagForm, self).save(commit=commit)

class MachineTagForm(AddForeginMember):
    member_fk = "contact"
    
    class Meta:
        model = MachineTag
        exclude = ('print_date', 'visible', )
        
    def save(self, commit=True):
        tag = super(MachineTagForm, self).save(commit=False)
        tag.print_date = timezone.now()
        return super(MachineTagForm, self).save(commit=commit)

