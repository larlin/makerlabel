from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.views.generic.detail import SingleObjectMixin
from subprocess import Popen, PIPE
import tempfile
import os
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic

from .models import MemberBoxTag
from .models import Member
from .models import MemberBaseTag
from .models import BaseTag
from .forms import MemberBoxTagForm

# Create your views here.
    
class DetailView(generic.DetailView):
    model = MemberBoxTag
    context_object_name = 'tag'
    
    def get_queryset(self):
        return BaseTag.objects.select_subclasses()
        
class MemberDetailView(SingleObjectMixin, generic.ListView):
    model = Member
    #context_object_name = 'tags'
    template_name = 'tags/member_detail.html'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Member.objects.all())
        return super(MemberDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MemberDetailView, self).get_context_data(**kwargs)
        context['member'] = self.object
        return context

    def get_queryset(self):
        print(dir(self.object))
        return self.object.memberbasetag_set.filter(visible=True).order_by('-print_date').select_subclasses()
    
class TagListView(generic.ListView):
    model = BaseTag
    context_object_name = 'tags'
	
    def get_queryset(self):
        return BaseTag.objects.filter(visible=True).order_by('-print_date').select_subclasses()

class MemberListView(generic.ListView):
    model = Member
    context_object_name = 'members'

class Add(generic.CreateView):
    model = MemberBoxTag
    fields = '__all__'
    template_name = 'tags/add.html'
    form_class = MemberBoxTagForm
    
    def get_initial(self, **kwargs):
        if 'member_id' in self.kwargs:
            print (self.kwargs['member_id'])
            return { 'member_id' : self.kwargs['member_id'] }
        return {}

class Delete(generic.DeleteView):
    model = MemberBoxTag
    success_url = reverse_lazy('tags:list')
    template_name = 'tags/delete.html'
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.visible = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

def download(request, tag_id):
    tag = get_object_or_404(MemberBoxTag, pk=tag_id)

    with tempfile.TemporaryDirectory() as tempdir:
        filename = tag.generate_pdf(tempdir, get_template('latex/ladtagA6.tex'), request.META['HTTP_HOST'])
        with open(os.path.join(tempdir, filename), 'rb') as f:
            pdf = f.read()
     
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    
    return response

def print_pdf(request, tag_id):
    tag = get_object_or_404(MemberBoxTag, pk=tag_id)
    with tempfile.TemporaryDirectory() as tempdir:        
        tempfilename = tag.generate_pdf(tempdir, get_template('latex/ladtagA6.tex'), request.META['HTTP_HOST'])
        
        #lp ladtagA6.pdf -o media=A5 -o landscape -o sides=two-sides-long-edge -o number-up=2 -o fit-to-page
        #lp ladtagA6.pdf -o media=A4 -o landscape -o sides=two-sides-long-edge -o number-up=4 -o fit-to-page
        #            ['lp', tempfilename, '-o', 'media=A5', '-o', 'landscape', '-o', 'sides=two-sides-long-edge',
        #    '-o', 'number-up=2', '-o', 'fit-to-page'],
        printprocess = Popen(
            ['lp', tempfilename, '-o', 'media=A4', '-o', 'portrait', '-o', 'sides=two-sides-long-edge',
            '-o', 'number-up=4', '-o', 'fit-to-page'],
            stdin=PIPE,
            stdout=PIPE,
            cwd=tempdir
        )
        printprocess.wait()
    return HttpResponseRedirect(reverse('tags:details_long', args=(tag_id,)))

