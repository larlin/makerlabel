from django.db import models
from django.template import Context
from subprocess import Popen, PIPE
import os
import shutil
import tags

# Create your models here.

class Tag(models.Model):
    user_id = models.IntegerField(default=0)
    box_number = models.IntegerField(default=0)
    name = models.CharField(max_length=20)  
    print_date = models.DateField('print date')
    comment = models.CharField(max_length=50)
    def get_absolute_url(self):
    	from django.core.urlresolvers import reverse
    	return reverse('tags:details_long', args=[str(self.id)])
    
    sentinel = object()
    def generate_pdf(self, work_directory, template, destination=sentinel):
        if destination is self.sentinel:
            destination = work_directory
        
        # TODO: Create a fancy name for the pdf with the member name and box number.
        # Remember to remove spaces from name.
        filename = "{}-{}.pdf".format(self.user_id, self.box_number)
        
        #filename = "document"
        # Render latex from template provided
        context = Context({ 'tag': self,})
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

