from django import forms

from .models import Client


class DateInput(forms.DateInput):
    input_type = 'date'


class ClientForm(forms.ModelForm):
    # Field layout for the dashboard form — (title, icon, [field names])
    SECTIONS = [
        ('Client Details', 'ri-user-line',
         ['name', 'company_name', 'email', 'phone_number', 'whatsapp_number', 'gst_number']),
        ('Address', 'ri-map-pin-line',
         ['address', 'city', 'state', 'country', 'pincode']),
        ('Project & Service', 'ri-code-box-line',
         ['service_type', 'project_title', 'status', 'priority', 'project_url', 'domain_name',
          'hosting_provider', 'domain_expiry_date', 'hosting_expiry_date', 'description']),
        ('Pricing & Payment', 'ri-money-rupee-circle-line',
         ['currency', 'quoted_amount', 'discount', 'final_amount', 'amount_paid',
          'payment_status', 'payment_terms', 'invoice_number', 'price_detail']),
        ('Timeline', 'ri-calendar-line',
         ['proposed_on', 'confirmation_date', 'project_start_date', 'completion_target_date',
          'completed_on', 'delivery_date', 'renewal_date']),
        ('Documents', 'ri-file-list-3-line',
         ['quotation_file', 'agreement_file', 'invoice_file']),
        ('Internal', 'ri-sticky-note-line',
         ['source', 'inquiry', 'assigned_to', 'notes', 'is_active']),
    ]
    FULL_WIDTH = {'address', 'description', 'price_detail', 'notes', 'is_active'}

    class Meta:
        model = Client
        exclude = ('client_id', 'created_at', 'updated_at')
        widgets = {
            'proposed_on':            DateInput(),
            'confirmation_date':      DateInput(),
            'project_start_date':     DateInput(),
            'completion_target_date': DateInput(),
            'completed_on':           DateInput(),
            'delivery_date':          DateInput(),
            'renewal_date':           DateInput(),
            'domain_expiry_date':     DateInput(),
            'hosting_expiry_date':    DateInput(),
            'address':      forms.Textarea(attrs={'rows': 2}),
            'description':  forms.Textarea(attrs={'rows': 4}),
            'price_detail': forms.Textarea(attrs={'rows': 4}),
            'notes':        forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput, forms.FileInput, forms.ClearableFileInput)):
                continue
            widget.attrs.setdefault('class', 'f-input')
            if not widget.attrs.get('placeholder') and isinstance(widget, (forms.TextInput, forms.Textarea)):
                widget.attrs['placeholder'] = field.label

        self.fields['final_amount'].required = False
        self.fields['final_amount'].help_text = 'Leave blank to auto-calculate (quoted − discount)'

    def clean(self):
        cleaned = super().clean()
        start  = cleaned.get('project_start_date')
        target = cleaned.get('completion_target_date')
        done   = cleaned.get('completed_on')

        if start and target and target < start:
            self.add_error('completion_target_date', 'Target date cannot be before the project start date.')
        if start and done and done < start:
            self.add_error('completed_on', 'Completion date cannot be before the project start date.')

        quoted   = cleaned.get('quoted_amount') or 0
        discount = cleaned.get('discount') or 0
        if discount > quoted:
            self.add_error('discount', 'Discount cannot be greater than the quoted amount.')

        final = cleaned.get('final_amount') or (quoted - discount)
        cleaned['final_amount'] = final
        if (cleaned.get('amount_paid') or 0) > final:
            self.add_error('amount_paid', 'Amount paid cannot exceed the final amount.')

        return cleaned

    def sections(self):
        """Yield the form grouped into labelled sections for the dashboard template."""
        for title, icon, names in self.SECTIONS:
            yield {
                'title': title,
                'icon': icon,
                'items': [{'field': self[n], 'full': n in self.FULL_WIDTH}
                          for n in names if n in self.fields],
            }
