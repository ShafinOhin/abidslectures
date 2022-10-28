from email.policy import default
from random import choices
from secrets import choice
from django.db import models

from accounts.models import Account

class Number(models.Model):
    bkash_number = models.CharField(max_length = 15, blank = True, null = True)
    rocket_number = models.CharField(max_length = 15, blank = True, null = True)

    def __str__(self):
        return self.bkash_number + '   |   ' + self.rocket_number


class Order(models.Model):
    user = models.ForeignKey(Account, on_delete = models.SET_NULL, blank = True, null = True)
    required_amount = models.CharField(max_length = 20, default = 0)
    STATUS_CHOICES = (
        ('P', 'Processing'),
        ('R', 'Rejected'),
        ('A', 'Approved'),
        ('D', 'Dismissed')
    )

    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default = 'P')
    comment_for_user = models.TextField(max_length = 250, default = "Your Payment is processing, please wait for us to update the received amount.", blank = True, null = True)
    date_placed = models.DateTimeField(auto_now_add = True, blank = True, null = True)

    @property
    def display_status(self):
        if self.status == 'A':
            return 'Approved'
        elif self.statys == 'P':
            return 'Processing'
        elif self.status == 'R':
            return 'Rejected'
        elif self.status == 'D':
            return 'Dismissed'
    
    @property
    def get_received_amount(self):
        rec_amount = 0
        for transaction in self.transaction_set.filter(is_validated = True):
            rec_amount += int(transaction.sent_amount)
        return rec_amount

    def get_remaining_amount(self):
        rec_amount = self.get_received_amount
        rem_amount = int(self.required_amount) - rec_amount
        return rem_amount

    ### To change order status to Approved
    def update_order(self):
        rem_amount = self.get_remaining_amount()
        if rem_amount <= 0:
            self.status = 'A'
            for sub in self.subscription_set.all():
                sub.active = True
                sub.save()
        

    ### Be careful with this function. Pricing of units might change later. Order amount should not change
    def update_required_amount(self):
        req_amount = 0
        for subscription in self.subscription_set.all():
            if subscription.subscription_type == 0:
                req_amount += int(subscription.course.course_price)
            elif subscription.subscription_type == 1:
                req_amount += int(subscription.unit.unit_price)
        self.required_amount = req_amount

    def __str__(self):
        return self.status + ' | ' + ' Rem: ' + str(self.get_remaining_amount())
    



class Transaction(models.Model):
    sender_number = models.CharField(max_length = 15, blank = True, null = True)
    trxID = models.CharField(max_length = 25, blank = True, null = True)
    sent_amount = models.CharField(max_length = 20, default = 0)
    submit_time = models.DateTimeField(auto_now_add = True)

    ## Set this true after manual validation
    is_validated = models.BooleanField(default = False)

    ## For partial transaction
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, blank = True, null = True)

    def __str__(self):
        return self.sender_number + ' | ' + self.trxID + ' | '


