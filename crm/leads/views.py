from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadModelForm

# Create your views here.

def lead_list(request):
    leads=Lead.objects.all()
    context={
        'leads':leads
    }
    return render(request,'leads/lead_list.html',context)



def lead_detail(request,id):
    lead=Lead.objects.get(id=id)
    context={
        'lead':lead
    }
    return render(request,'leads/lead_detail.html',context)



def lead_create(request):
    form=LeadModelForm()
    if request.method == 'POST':
        form=LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leads:lead_list')
    context={
            'form':form
        }
    return render(request,'leads/lead_create.html',context)

