from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect
from subprocess import Popen, PIPE
import tempfile
import os
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.conf import settings

from .models import MemberBoxTag
from .models import Member
from .models import MemberBaseTag
from .models import MachineTag
from .models import BaseTag
from .models import Comment
from .forms import MemberBoxTagForm
from .forms import MachineTagForm

# Create your views here.

class MainView(generic.ListView):
    model = Member
    template_name = 'tags/main.html'
    context_object_name = 'members'
    
    def get_context_data(self, *args, **kwargs):
        context = super(MainView, self).get_context_data(*args, **kwargs)
        context['machines'] = MachineTag.objects.all()
        return context 

# Member views

class MemberDetailView(SingleObjectMixin, generic.ListView):
    model = Member
    template_name = 'tags/member_detail.html'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Member.objects.all())
        return super(MemberDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MemberDetailView, self).get_context_data(**kwargs)
        context['member'] = self.object
        return context

    def get_queryset(self):
        return self.object.memberbasetag_set.filter(visible=True).order_by('-print_date').select_subclasses()
        
class MemberListView(generic.ListView):
    model = Member
    context_object_name = 'members'

# Machine views

class MachineTagAdd(generic.CreateView):
    model = MachineTag
    fields = '__all__'
    template_name = 'tags/add_machine_tag.html'
    form_class = MachineTagForm
    
    def get_initial(self, **kwargs):
        if 'contact' in self.kwargs:
            print (self.kwargs['contact'])
            return { 'contact' : self.kwargs['contact'] }
        return {}

class MachineTagDetailView(SingleObjectMixin, generic.ListView):
    model = MachineTag
    template_name = 'tags/machinetag_detail.html'
    context_object_name = 'tag'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=MachineTag.objects.all())
        return super(MachineTagDetailView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(MachineTagDetailView, self).get_context_data(**kwargs)
        context['machine_tag'] = self.object
        return context
        
    def get_queryset(self):
        return self.object.comment_set.all()

# Comment views

class CommentAdd(generic.CreateView):
    model = Comment
    fields = '__all__'
    template_name = 'tags/addComment.html'
    context_object_name = 'comment'
    
    def get_initial(self, **kwargs):
        if 'machine' in self.kwargs:
            print("Found machine")
            return { 'machine' : self.kwargs['machine'] }
        return {}

# Tag views

class DetailView(generic.DetailView):
    model = MemberBoxTag
    context_object_name = 'tag'
    
    def render_to_response(self, context):
        
        # TODO: Try to fix hacky solution to forwarding to MachineTagDetailView.
        # Hacky solution to forward machines to the right view to get comments to work.
        # Probably possible to create a better solution
        if isinstance(context['object'], MachineTag):
            print(context)
            from django.core.urlresolvers import reverse
            return redirect(reverse('tags:machine_tag_details', args=[str(context['object'].id)]))
        

        return super(DetailView, self).render_to_response(context)
    
    def get_queryset(self):
        return BaseTag.objects.select_subclasses()


class ListView(generic.ListView):
    model = BaseTag
    context_object_name = 'tags'
	
    def get_queryset(self):
        return BaseTag.objects.filter(visible=True).order_by('-print_date').select_subclasses()


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

class DownloadView(generic.View):
    def get(self, request, tag_id):
        tag = get_object_or_404(BaseTag.objects.select_subclasses(), pk=tag_id)
        
        with tempfile.TemporaryDirectory() as tempdir:
            filename = tag.generate_pdf(tempdir, request.META['HTTP_HOST'])
            with open(os.path.join(tempdir, filename), 'rb') as f:
                pdf = f.read()
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        
        return response

class PrintView(generic.View):
    def get(self, request, tag_id):
        tag = get_object_or_404(MemberBoxTag, pk=tag_id)
        with tempfile.TemporaryDirectory() as tempdir:        
            tempfilename = tag.generate_pdf(tempdir, request.META['HTTP_HOST'])
            
            #lp ladtagA6.pdf -o media=A5 -o landscape -o sides=two-sides-long-edge -o number-up=2 -o fit-to-page
            #lp ladtagA6.pdf -o media=A4 -o landscape -o sides=two-sides-long-edge -o number-up=4 -o fit-to-page
            #            ['lp', tempfilename, '-o', 'media=A5', '-o', 'landscape', '-o', 'sides=two-sides-long-edge',
            #    '-o', 'number-up=2', '-o', 'fit-to-page'],
            
            printer = ""
            
            if hasattr(settings.DEBUG, 'PRINTERS'):
                printer = "-P "+settings.DEBUG['paper-printer']
            
            printprocess = Popen(
                ['lp', tempfilename, '-o', 'media=A4', '-o', 'portrait', '-o', 'sides=two-sides-long-edge',
                '-o', 'number-up=4', '-o', 'fit-to-page'],
                stdin=PIPE,
                stdout=PIPE,
                cwd=tempdir
            )
            printprocess.wait()
        return HttpResponseRedirect(reverse('tags:details_long', args=(tag_id,)))

