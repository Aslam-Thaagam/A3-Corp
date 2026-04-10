from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
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


def sample(request):
    return render(request, 'sample.html')


def sample_gym(request):
    return render(request, 'samples/gym.html')


def sample_restaurant(request):
    return render(request, 'samples/restaurant.html')


def sample_portfolio(request):
    return render(request, 'samples/portfolio.html')


def sample_petshop(request):
    return render(request, 'samples/petshop.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        service = request.POST.get('services', '')
        message = request.POST.get('message', '').strip()

        if not name or not email or not subject or not message:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'contact.html')  # noqa

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


@login_required
def dashboard(request):
    filter_by = request.GET.get('filter', 'all')
    search    = request.GET.get('q', '').strip()

    qs = Contact.objects.all()
    if search:
        from django.db.models import Q
        qs = qs.filter(Q(name__icontains=search) | Q(email__icontains=search) | Q(subject__icontains=search))
    if filter_by == 'unread':
        qs = qs.filter(is_read=False)
    elif filter_by == 'read':
        qs = qs.filter(is_read=True)

    now = timezone.now()
    total      = Contact.objects.count()
    unread     = Contact.objects.filter(is_read=False).count()
    this_month = Contact.objects.filter(created_at__year=now.year, created_at__month=now.month).count()

    return render(request, 'dashboard.html', {
        'contacts':   qs,
        'total':      total,
        'unread':     unread,
        'this_month': this_month,
        'filter_by':  filter_by,
        'search':     search,
    })


@login_required
def mark_read(request, pk):
    if request.method == 'POST':
        contact = get_object_or_404(Contact, pk=pk)
        contact.is_read = True
        contact.save()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=400)


@login_required
def delete_contact(request, pk):
    if request.method == 'POST':
        get_object_or_404(Contact, pk=pk).delete()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
