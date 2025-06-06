from django.shortcuts import render,redirect, reverse
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadModelForm
from django.views import generic
from django.core.mail import send_mail

# Create your views here.

# def lead_list(request):
#     leads=Lead.objects.all()
#     context={
#         'leads':leads
#     }
#     return render(request,'leads/lead_list.html',context)



# def lead_detail(request,id):
#     lead=Lead.objects.get(id=id)
#     context={
#         'lead':lead
#     }
#     return render(request,'leads/lead_detail.html',context)



# def lead_create(request):
#     form=LeadModelForm()
#     if request.method == 'POST':
#         form=LeadModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('leads:lead_list')
#     context={
#             'form':form
#         }
#     return render(request,'leads/lead_create.html',context)


# def lead_update(request,id):
#     lead=Lead.objects.get(id=id)
#     form=LeadModelForm(instance=lead)
#     if request.method == 'POST':
#         form=LeadModelForm(request.POST, instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect('leads:lead_list')
#     context={
#         'lead':lead,
#         'form':form
#     }
#     return render(request,'leads/lead_update.html',context)



# def lead_delete(request,id):
#     lead=Lead.objects.get(id=id)
#     lead.delete()
#     return redirect('leads:lead-list')



# def landing_page(request):
#     return render(request, "landing.html")


class LandingPageView(generic.TemplateView):
    template_name="landing.html"


class LeadListView(generic.ListView):
    template_name="leads/lead_list.html"
    queryset=Lead.objects.all()
    context_object_name="leads"


class leadCreateView(generic.CreateView):
    template_name="leads/lead_create.html"
    form_class=LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list") 
    
    def form_valid(self, form):
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(leadCreateView,self).form_valid(form)
    

class LeadDetailView(generic.DetailView):
    template_name="leads/lead_detail.html"
    queryset=Lead.objects.all()
    context_object_name="lead"


class LeadUpdateView(generic.UpdateView):
    template_name="leads/lead_update.html"
    queryset=Lead.objects.all()
    form_class=LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    

class LeadDeleteView(generic.DeleteView):
    template_name="leads/lead_delete.html"
    queryset=Lead.objects.all()


    def get_success_url(self):
        return reverse("leads:lead-list")