from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
import datetime

class RenewBookForm(forms.Form):
    renewaldate = forms.DateField(help_text="Enter a date between now and 4 weeks", required=False)
    
    def clean_renewaldate(self):
        data = self.cleaned_data['renewaldate']
        
        if data<datetime.date.today():
            raise ValidationError(_("Invalid date: its in past dummy"))
        
        elif data>datetime.date.today()+datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date: its more than 4 weeks"))

        return data