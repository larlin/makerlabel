from django.db import models
from django.template import Context
from subprocess import Popen, PIPE
from model_utils.managers import InheritanceManager
import os
import shutil
import tags

# Create your models here.

class Member(models.Model):
    name = models.CharField(max_length=20)
    member_number = models.IntegerField(default=0)
    box_num = models.IntegerField(default=0)
	
    def __unicode__( self ):
        return "{0}".format( self.name)
    
    def __str__( self ):
        return "{0}".format( self.name )


class BaseTag(models.Model):
    print_date = models.DateField('print date')
    visible = models.BooleanField(default=True)
    objects = InheritanceManager()

class MachineTag(BaseTag):
    name = models.CharField(max_length=50, blank=False)
    contact = models.ForeignKey('Member')
    info = models.CharField(max_length=400, blank=True)
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('tags:machine_tag_details', args=[str(self.id)])
    
    def __str__( self ):
        return self.name
    
    def __unicode__( self ):
        return self.name

class Comment(models.Model):
    writer = models.ForeignKey('Member')
    machine = models.ForeignKey('MachineTag')
    commentText = models.CharField(max_length=400)

class MemberBaseTag(BaseTag):
    member_id = models.ForeignKey('Member')
    comment = models.CharField(max_length=50, blank=True)
    objects = InheritanceManager()
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('tags:details_long', args=[str(self.id)])
    	
    def __str__( self ):
        return self.get_formated_name()
    
    def __unicode__( self ):
        return self.get_formated_name()
    
    def get_formated_name( self ):
        return self.member_id.name.replace(" ", "_")

class MemberShelfTag(MemberBaseTag):
    def __str__( self ):
        return self.get_formated_name()+"(hylla)"
    
    def __unicode__( self ):
        return self.get_formated_name()+"(hylla)"

class MemberBoxTag(MemberBaseTag):
    box_number = models.IntegerField(default=0)
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('tags:details_long', args=[str(self.id)])
    
    def __str__( self ):
        return "{}({})".format(self.get_formated_name(), self.box_number)
    
    def __unicode__( self ):
        return "{}({})".format(self.get_formated_name(), self.box_number)
        
    sentinel = object()
    def generate_pdf(self, work_directory, template, url, destination=sentinel):
        if destination is self.sentinel:
            destination = work_directory
        
        filename = "{}({})".format(self.get_formated_name(), self.box_number)
        
        # Render latex from template provided
        context = Context({ 'tag': self, 'url':'{}/{}'.format(url, self.pk)})
        rendered_tpl = template.render(context).encode('utf-8')
        
        # Copy files needed for the latex run to the work directory.
        latex_static_dir = os.path.dirname(tags.__file__) + "/latex_static/"
        for file_name in os.listdir(latex_static_dir):
            print ("Copying: "+file_name+" to "+work_directory)
            shutil.copy(latex_static_dir+"/"+file_name, work_directory)
        
        # Run pdflatex twice, for complete rendering of TOC and such.
        for i in range(2):
            process = Popen(
                ['pdflatex', '-output-directory', destination, '--jobname', filename],
                stdin=PIPE,
                stdout=PIPE,
                cwd=work_directory
            )
            process.communicate(rendered_tpl)
        
        return filename+".pdf"

