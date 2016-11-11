from django.template.loader import get_template
from subprocess import Popen, PIPE
import os
import shutil

class GeneratePdf:
    latex_static_dir = ""
    
    def __init__(self, latex_static_dir):
        self.latex_static_dir = latex_static_dir
    
    def generate(self, template_name, filename, context, work_directory, url, destination):
        template = get_template(template_name)
        
        # Render latex from template provided
        rendered_tpl = template.render(context).encode('utf-8')
        
        # Copy files needed for the latex run to the work directory.
        for file_name in os.listdir(self.latex_static_dir):
            print ("Copying: "+file_name+" to "+work_directory)
            shutil.copy(self.latex_static_dir+"/"+file_name, work_directory)
        
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

