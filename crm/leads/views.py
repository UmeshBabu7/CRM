from django.shortcuts import render,redirect, reverse
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadModelForm, CustomUserCreationForm, AssignAgentForm
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginRequiredMixin

# Create your views here.

class LandingPageView(generic.TemplateView):
    template_name="landing.html"


class LeadListView(LoginRequiredMixin,generic.ListView):
    template_name="leads/lead_list.html"
    context_object_name="leads"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
             queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, 
                agent__isnull=False
            )
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset
            })
        return context


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
    

class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
        
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)