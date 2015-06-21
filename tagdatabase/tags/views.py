from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from subprocess import Popen, PIPE
import tempfile
import os
import shutil
import tags
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.edit import CreateView

from .models import Tag
from .forms import TagForm

# Create your views here.
    
class DetailView(generic.DetailView):
    model = Tag
    template_name = 'tags/details.html'
    context_object_name = 'tag'
    
class ListView(generic.ListView):
    model = Tag
    template_name = 'tags/list.html'
    context_object_name = 'tag_list'
	
    def get_queryset(self):
        return Tag.objects.order_by('-print_date')
	
class Add(CreateView):
    model = Tag
    fields = '__all__'
    template_name = 'tags/add.html'
    form_class = TagForm

def download(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    template = get_template('latex/ladtagA6.tex')
    context = Context({ 'tag': tag,})
    rendered_tpl = template.render(context).encode('utf-8')
    
    with tempfile.TemporaryDirectory() as tempdir:
        # Create subprocess, supress output with PIPE and 
        # run latex twice to generate the TOC properly. 
        # Finally read the generated pdf.
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        # Copy files needed for the latex run to the temp directory.
        latex_static_dir = os.path.dirname(tags.__file__) + "/latex_static/"
        shutil.copy(latex_static_dir+"makerlkpg-cut.png", tempdir)
        shutil.copy(latex_static_dir+"qrcode.sty", tempdir)
        # Run pdflatex twice, for complete rendering of TOC and such.
        for i in range(2):
            process = Popen(
                ['pdflatex', '-output-directory', tempdir, '--jobname', 'ladtagA6'],
                stdin=PIPE,
                stdout=PIPE,
                cwd=tempdir
            )
            process.communicate(rendered_tpl)
            # Read the generated pdf to a variable.
            with open(os.path.join(tempdir, 'ladtagA6.pdf'), 'rb') as f:
                pdf = f.read()
     
    # TODO: Create a fancy name for the pdf with the member name and box number.
    # Remember to remove spaces from name.
    pdffile = "{}-{}.pdf".format(tag.user_id, tag.box_number)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(pdffile)
    
    return response

def print_pdf(request, tag_id):
    # Might not be the most buitiful solution but anyway....
    # This view will download the pdf from the download view
    # and then print it with lp to the local default printer...
    tag = get_object_or_404(Tag, pk=tag_id)
    with tempfile.TemporaryDirectory() as tempdir:
        tempfilename = "file.pdf"
        url = request.get_host()
        dlprocess = Popen(
            ['wget', '--output-document', tempfilename, url+reverse('tags:download', args=(tag.pk,))],
            stdin=PIPE,
            stdout=PIPE,
            cwd=tempdir
        )
        dlprocess.wait()
        
        #lp ladtagA6.pdf -o media=A5 -o landscape -o sides=two-sides-long-edge -o number-up=2 -o fit-to-page
        printprocess = Popen(
            ['lp', tempfilename, '-o', 'media=A5', '-o', 'landscape', '-o', 'sides=two-sides-long-edge',
            '-o', 'number-up=2', '-o', 'fit-to-page'],
            stdin=PIPE,
            stdout=PIPE,
            cwd=tempdir
        )
        printprocess.wait()
    return HttpResponseRedirect(reverse('tags:details_long', args=(tag_id,)))

