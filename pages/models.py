from django.db import models
from django.contrib.auth.models import User as user

class CashMoneyChoices(models.Model):
    # Define your enum choices as class attributes
    BILL_COMPANIES_CHOICES = [
        ('1', 'Electricity'),
        ('2', 'Water'),
        ('3', 'Phone'),
    ]

    USER_ROLES_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('superadmin', 'Manage'),
    ]
    
    TRANSACTION_TYPE_CHOICES = [
        ('1', 'Deposit'),
        ('2', 'Withdrawal'),
        ('3', 'Transfer'),
    ]

    STATUS_CHOICES = [
        ('1', 'Pending'),
        ('2', 'Completed'),
        ('3', 'Failed'),
    ]

    LOG_STATUS_CHOICES = [
        ('1', 'Deposit'),
        ('2', 'Withdrawal'),
        ('3', 'Transfer'),
        ('4','Bill Payment'),
        ('5','Ticket Payment'),
        ('6','Login'),
        ('7','Create Account'),
        ('8','LogOut')
    ]
   
    bill_company = models.CharField(max_length= 100, choices=BILL_COMPANIES_CHOICES)
    user_role = models.CharField(max_length=10, choices=USER_ROLES_CHOICES)


class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    account_status = models.BooleanField(default=True)  


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(user, related_name='sent_transactions', on_delete=models.CASCADE,default=None)
    receiver = models.ForeignKey(user, related_name='received_transactions', on_delete=models.CASCADE,default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(choices=CashMoneyChoices.TRANSACTION_TYPE_CHOICES, default='1')
    status = models.CharField(choices=CashMoneyChoices.STATUS_CHOICES, default='2')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_type}"



class BillPayment(models.Model):
    bill_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE,blank=True)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bill_type = models.CharField(choices=CashMoneyChoices.BILL_COMPANIES_CHOICES,max_length=255)  
    payment_status = models.CharField(choices=CashMoneyChoices.STATUS_CHOICES,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
  

class Staduims(models.Model):
    Staduim_id = models.AutoField(primary_key=True)
    Staduim_name = models.CharField(max_length=50,unique=True)
    Ticket_Price = models.DecimalField(max_digits=10, decimal_places=2,default=10.00)
    Capacity = models.IntegerField() 

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    Stauim_name = models.ForeignKey(Staduims, to_field='Staduim_name', on_delete=models.CASCADE)
    status = models.CharField(choices=CashMoneyChoices.STATUS_CHOICES,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Log(models.Model):
    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(user, null=True, blank=True, on_delete=models.CASCADE)
    log_type = models.CharField(choices=CashMoneyChoices.LOG_STATUS_CHOICES)  
    timestamp = models.DateTimeField(auto_now_add=True)

# class Offer(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     start_date = models.DateField()
#     end_date = models.DateField()
#     discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.title

# class Numbers(models.Model):
#     Vodafone_Numbers=models.CharField(max_length=12)
#     Etisalat_Numbers=models.CharField(max_length=12)
#     Orange_Numbers=models.CharField(max_length=12)

#     class Meta:
#         using = "Numbers"