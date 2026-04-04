from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact, Service


def index(request):
    services = Service.objects.filter(is_active=True)[:6]
    return render(request, 'index.html', {'services': services})


def about(request):
    return render(request, 'about.html')


def services(request):
    all_services = Service.objects.filter(is_active=True)
    return render(request, 'services.html', {'services': all_services})


def products(request):
    return render(request, 'products.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        service = request.POST.get('services', '')
        message = request.POST.get('message', '').strip()

        if not name or not email or not subject or not message:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'contact.html')

        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            services=service,
            message=message,
        )
        messages.success(request, 'Thank you! Your message has been received. We will get back to you shortly.')
        return redirect('contact')

    return render(request, 'contact.html')
