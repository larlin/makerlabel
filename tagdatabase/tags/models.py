from django.db import models
from django.template import Context
from subprocess import Popen, PIPE
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
    
    class Meta:
        abstract = True

class MemberBaseTag(BaseTag):
    member_id = models.ForeignKey('Member')
    comment = models.CharField(max_length=50, blank=True)
    visible = models.BooleanField(default=True)
    
    def get_absolute_url(self):
    	from django.core.urlresolvers import reverse
    	return reverse('tags:details_long', args=[str(self.basetag.id)])
    	
    def __str__( self ):
        return self.get_formated_name()
    
    def __unicode__( self ):
        return self.get_formated_name()
    
    def get_formated_name( self ):
        return self.member_id.name.replace(" ", "_")

class MemberShelfTag(MemberBaseTag):
    def __str__( self ):
        return self.get_formated_name()
    
    def __unicode__( self ):
        return self.get_formated_name()

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
        shutil.copy(latex_static_dir+"MakersLink-line-color.png", work_directory)
        shutil.copy(latex_static_dir+"qrcode.sty", work_directory)
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

