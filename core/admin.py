from django.contrib import admin
from core.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'name', 'amount', 'transaction_status']
