from django.contrib import admin
from .models import Contact, Service, Inquiry, Client


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'selected_service', 'created_at')
    list_filter = ('selected_service', 'created_at')
    search_fields = ('name', 'email')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'name', 'company_name', 'service_type', 'status',
                    'final_amount', 'amount_paid', 'balance_due', 'payment_status',
                    'completion_target_date', 'completed_on')
    list_filter = ('status', 'payment_status', 'priority', 'service_type', 'is_active',
                   'proposed_on', 'confirmation_date', 'completed_on')
    search_fields = ('client_id', 'name', 'company_name', 'email', 'phone_number',
                     'project_title', 'invoice_number', 'domain_name')
    date_hierarchy = 'created_at'
    readonly_fields = ('client_id', 'balance_due', 'duration_days', 'created_at', 'updated_at')
    list_editable = ('status', 'payment_status')
    autocomplete_fields = ('service_type',)
    fieldsets = (
        ('Client Details', {
            'fields': ('client_id', 'name', 'company_name', 'email', 'phone_number',
                       'whatsapp_number', 'gst_number')
        }),
        ('Address', {
            'classes': ('collapse',),
            'fields': ('address', 'city', 'state', 'country', 'pincode')
        }),
        ('Project', {
            'fields': ('service_type', 'project_title', 'description', 'status', 'priority',
                       'project_url', 'domain_name', 'hosting_provider',
                       'domain_expiry_date', 'hosting_expiry_date')
        }),
        ('Pricing', {
            'fields': ('currency', 'quoted_amount', 'discount', 'final_amount', 'amount_paid',
                       'balance_due', 'payment_status', 'payment_terms', 'price_detail',
                       'invoice_number')
        }),
        ('Timeline', {
            'fields': ('proposed_on', 'confirmation_date', 'project_start_date',
                       'completion_target_date', 'completed_on', 'delivery_date',
                       'renewal_date', 'duration_days')
        }),
        ('Documents', {
            'fields': ('quotation_file', 'agreement_file', 'invoice_file')
        }),
        ('Internal', {
            'fields': ('source', 'inquiry', 'assigned_to', 'notes', 'is_active',
                       'created_at', 'updated_at')
        }),
    )
