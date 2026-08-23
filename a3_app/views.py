from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Q, Sum, Count

from . import seo as seo_conf
from .forms import ClientForm
from .models import Contact, Service, Client


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


# ─────────────────────────────  CLIENTS  ─────────────────────────────

@login_required
def client_list(request):
    status  = request.GET.get('status', 'all')
    payment = request.GET.get('payment', '')
    search  = request.GET.get('q', '').strip()

    qs = Client.objects.select_related('service_type')

    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(company_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone_number__icontains=search) |
            Q(project_title__icontains=search) |
            Q(client_id__icontains=search)
        )
    if status == 'overdue':
        qs = qs.filter(completed_on__isnull=True,
                       completion_target_date__lt=timezone.localdate())
    elif status != 'all':
        qs = qs.filter(status=status)
    if payment:
        qs = qs.filter(payment_status=payment)

    all_clients = Client.objects.all()
    totals = all_clients.aggregate(billed=Sum('final_amount'), received=Sum('amount_paid'))
    billed   = totals['billed']   or 0
    received = totals['received'] or 0

    status_counts = {row['status']: row['n']
                     for row in all_clients.values('status').annotate(n=Count('id'))}
    status_tabs = [(value, label, status_counts.get(value, 0))
                   for value, label in Client.Status.choices]
    overdue_count = all_clients.filter(completed_on__isnull=True,
                                       completion_target_date__lt=timezone.localdate()).count()

    return render(request, 'dashboard_clients.html', {
        'clients':        qs,
        'total':          all_clients.count(),
        'active':         all_clients.filter(status__in=[Client.Status.CONFIRMED,
                                                         Client.Status.IN_PROGRESS]).count(),
        'completed':      status_counts.get(Client.Status.COMPLETED, 0),
        'billed':         billed,
        'received':       received,
        'outstanding':    billed - received,
        'overdue_count':  overdue_count,
        'status_tabs':    status_tabs,
        'payment_choices': Client.PaymentStatus.choices,
        'status':         status,
        'payment':        payment,
        'search':         search,
    })


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client.objects.select_related('service_type', 'assigned_to', 'inquiry'), pk=pk)
    return render(request, 'dashboard_client_detail.html', {'client': client})


@login_required
def client_create(request):
    form = ClientForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        client = form.save()
        messages.success(request, f'Client "{client.name}" added successfully.')
        return redirect('client_detail', pk=client.pk)
    return render(request, 'dashboard_client_form.html', {'form': form, 'is_edit': False})


@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, request.FILES or None, instance=client)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Client "{client.name}" updated.')
        return redirect('client_detail', pk=client.pk)
    return render(request, 'dashboard_client_form.html',
                  {'form': form, 'is_edit': True, 'client': client})


@login_required
def client_delete(request, pk):
    if request.method == 'POST':
        client = get_object_or_404(Client, pk=pk)
        name = client.name
        client.delete()
        messages.success(request, f'Client "{name}" deleted.')
    return redirect('client_list')


# ─────────────────────────────  SEO  ─────────────────────────────

def robots_txt(request):
    """Allow the public site, keep the dashboard and admin out of the index."""
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /dashboard/',
        'Disallow: /admin/',
        'Disallow: /media/clients/',
        '',
        f'Sitemap: {seo_conf.SITE_URL}/sitemap.xml',
        '',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')
