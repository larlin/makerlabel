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

from .models import Tag
from .forms import TagForm

# Create your views here.

def details(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    return render(request, 'tags/details.html', {'tag': tag})

def list(request):
    tag_list = Tag.objects.order_by('-print_date')
    context = {'tag_list': tag_list,}
    return render(request, 'tags/list.html', context)

def add(request):
	if request.method == 'POST':
		form = TagForm(request.POST)
		
		if form.is_valid():
			new_tag = form.save()
			return HttpResponseRedirect(reverse('tags:details_long', args=(new_tag.pk,)))
		else:
			form = TagForm()
	else:
		form = TagForm()
	return render(request, 'tags/add.html', {'form': form})

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

def print(requesst, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)

