from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Tax

# Register your models here.
class TaxHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["id", "tax_payer", "tax_accountant", "status", 'payment_status', 'history']
    history_list_display = ["status", 'history_date', 'history_user']

admin.site.register(Tax, TaxHistoryAdmin)

