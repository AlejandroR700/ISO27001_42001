from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Control, Risk
from .forms import ContactForm
from django.conf import settings

def home(request):
    return render(request, 'portal/home.html')

def features(request):
    return render(request, 'portal/features.html')

def security(request):
    controls = Control.objects.all().order_by('control_id')
    risks = Risk.objects.all()
    return render(request, 'portal/security.html', {'controls': controls, 'risks': risks})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # enviar correo (a consola en dev)
            subject = f"Contacto web - {form.cleaned_data['company'] or 'Sin empresa'}"
            body = f"Nombre: {form.cleaned_data['name']}\nEmail: {form.cleaned_data['email']}\n\nMensaje:\n{form.cleaned_data['message']}"
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, ['info@medidata.health'])
            return render(request, 'portal/contact_success.html', {'form': form.cleaned_data})
    else:
        form = ContactForm()
    return render(request, 'portal/home.html', {'contact_form': form})
