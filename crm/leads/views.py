from django.shortcuts import render,redirect, reverse
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadModelForm, CustomUserCreationForm
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin

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


class LeadListView(LoginRequiredMixin,generic.ListView):
    template_name="leads/lead_list.html"
    context_object_name="leads"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


class leadCreateView(LoginRequiredMixin,generic.CreateView):
    template_name="leads/lead_create.html"
    form_class=LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list") 
    
    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(leadCreateView,self).form_valid(form)
    

class LeadDetailView(LoginRequiredMixin,generic.DetailView):
    template_name="leads/lead_detail.html"
    context_object_name="lead"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


class LeadUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name="leads/lead_update.html"
    form_class=LeadModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")
    

class LeadDeleteView(LoginRequiredMixin,generic.DeleteView):
    template_name="leads/lead_delete.html"

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)
    


class SignupView(generic.CreateView):
    template_name="registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("leads:login")