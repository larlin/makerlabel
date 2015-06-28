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

class Tag(models.Model):
    member_id = models.ForeignKey('Member')
    box_number = models.IntegerField(default=0)
    print_date = models.DateField('print date')
    comment = models.CharField(max_length=50)
    visible = models.BooleanField(default=True)
    
    def get_absolute_url(self):
    	from django.core.urlresolvers import reverse
    	return reverse('tags:details_long', args=[str(self.id)])
    	
    def __unicode__( self ):
        return "{0}({1})".format( self.member_id, self.box_number )
    
    def __str__( self ):
        return "{0}({1})".format( self.member_id, self.box_number )
    
    sentinel = object()
    def generate_pdf(self, work_directory, template, url, destination=sentinel):
        if destination is self.sentinel:
            destination = work_directory
        
        # TODO: Create a fancy name for the pdf with the member name and box number.
        # Remember to remove spaces from name.
        filename = "{}({}).pdf".format(self.member_id.id, self.box_number)
        
        # Render latex from template provided
        context = Context({ 'tag': self, 'url':'{}/{}'.format(url, self.pk)})
        rendered_tpl = template.render(context).encode('utf-8')
        
        # Copy files needed for the latex run to the work directory.
        latex_static_dir = os.path.dirname(tags.__file__) + "/latex_static/"
        shutil.copy(latex_static_dir+"makerlkpg-cut.png", work_directory)
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

