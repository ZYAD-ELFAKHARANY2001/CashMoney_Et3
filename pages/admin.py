from django.contrib import admin

from .models import Transaction,BillPayment,Staduims,Ticket,CashMoneyChoices,Log,Account
admin.site.register(Transaction)
admin.site.register(BillPayment)
admin.site.register(Staduims)
admin.site.register(Ticket)
admin.site.register(CashMoneyChoices)
admin.site.register(Log)
admin.site.register(Account)