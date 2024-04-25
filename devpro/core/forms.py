from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm

from devpro.core.models import Borrow


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ("book", "user", "start_date", "end_date", "returned_at", "library")


class CustomAdminAuthenticationForm(AdminAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "E-mail"
