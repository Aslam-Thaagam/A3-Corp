from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=1000)
    services = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']


class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Inquiry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    selected_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    agreed_to_terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.selected_service}"


class Client(models.Model):
    """Full record of a client engagement — from proposal to project completion."""

    class Status(models.TextChoices):
        PROPOSED = 'proposed', 'Proposed'
        NEGOTIATING = 'negotiating', 'Negotiating'
        CONFIRMED = 'confirmed', 'Confirmed'
        IN_PROGRESS = 'in_progress', 'In Progress'
        ON_HOLD = 'on_hold', 'On Hold'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    class PaymentStatus(models.TextChoices):
        UNPAID = 'unpaid', 'Unpaid'
        ADVANCE_PAID = 'advance_paid', 'Advance Paid'
        PARTIAL = 'partial', 'Partially Paid'
        PAID = 'paid', 'Fully Paid'
        REFUNDED = 'refunded', 'Refunded'

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    # --- Identity / contact ---
    client_id = models.CharField(max_length=20, unique=True, blank=True,
                                 help_text='Auto-generated reference, e.g. A3-0001')
    name = models.CharField(max_length=255, verbose_name='Client Name')
    company_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True, default='India')
    pincode = models.CharField(max_length=10, blank=True)
    gst_number = models.CharField(max_length=20, blank=True, verbose_name='GST / Tax Number')

    # --- Project / service ---
    service_type = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='clients')
    project_title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, help_text='Scope of work / requirement details')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PROPOSED)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    project_url = models.URLField(blank=True, help_text='Live site / delivered project link')
    domain_name = models.CharField(max_length=255, blank=True)
    hosting_provider = models.CharField(max_length=255, blank=True)
    domain_expiry_date = models.DateField(null=True, blank=True)
    hosting_expiry_date = models.DateField(null=True, blank=True)

    # --- Pricing ---
    currency = models.CharField(max_length=10, default='INR')
    quoted_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                        help_text='Amount originally quoted')
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                       help_text='Agreed amount after discount')
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices,
                                      default=PaymentStatus.UNPAID)
    payment_terms = models.CharField(max_length=255, blank=True,
                                     help_text='e.g. 50% advance, 50% on delivery')
    price_detail = models.TextField(blank=True, help_text='Itemised price breakdown / notes')
    invoice_number = models.CharField(max_length=50, blank=True)

    # --- Timeline ---
    proposed_on = models.DateField(null=True, blank=True)
    confirmation_date = models.DateField(null=True, blank=True)
    project_start_date = models.DateField(null=True, blank=True)
    completion_target_date = models.DateField(null=True, blank=True)
    completed_on = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True, help_text='Handed over to the client')
    renewal_date = models.DateField(null=True, blank=True, help_text='AMC / maintenance renewal')

    # --- Files ---
    quotation_file = models.FileField(upload_to='clients/quotations/', blank=True, null=True,
                                      verbose_name='Quotation (image / PDF)')
    agreement_file = models.FileField(upload_to='clients/agreements/', blank=True, null=True)
    invoice_file = models.FileField(upload_to='clients/invoices/', blank=True, null=True)

    # --- Internal tracking ---
    source = models.CharField(max_length=100, blank=True,
                              help_text='How the client reached us — referral, Instagram, walk-in, etc.')
    inquiry = models.ForeignKey(Inquiry, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='clients', help_text='Inquiry this client came from')
    assigned_to = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_clients')
    notes = models.TextField(blank=True, help_text='Internal notes — not shown to the client')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        label = self.company_name or self.name
        return f"{label} - {self.project_title or self.service_type or 'Project'}"

    def save(self, *args, **kwargs):
        if not self.final_amount:
            self.final_amount = (self.quoted_amount or 0) - (self.discount or 0)
        super().save(*args, **kwargs)
        if not self.client_id:
            Client.objects.filter(pk=self.pk).update(client_id=f"A3-{self.pk:04d}")
            self.client_id = f"A3-{self.pk:04d}"

    @property
    def balance_due(self):
        return (self.final_amount or 0) - (self.amount_paid or 0)

    @property
    def is_overdue(self):
        """Target date passed but the project is not completed yet."""
        from django.utils import timezone
        if self.completed_on or not self.completion_target_date:
            return False
        return self.completion_target_date < timezone.localdate()

    @property
    def duration_days(self):
        if self.project_start_date and self.completed_on:
            return (self.completed_on - self.project_start_date).days
        return None
