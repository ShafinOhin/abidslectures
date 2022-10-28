from django.shortcuts import render, redirect

from payment.models import Order, Transaction
from django.contrib.auth.decorators import login_required


@login_required
def manager_dashboard(request):
    if not request.user.is_admin:
        return redirect('profile')
    processing_orders = Order.objects.filter(status = 'P')
    unvalidated_trans = Transaction.objects.filter(is_validated = False)
    context = {
        'processing_orders': processing_orders,
        'unvalidated_trans': unvalidated_trans,
    }
    return render(request, 'manager/manager_dashboard.html', context = context)


@login_required
def approve_trans(request):
    if not request.user.is_admin:
        return redirect('profile')
    
    trans_id = request.POST['transid']
    amount = request.POST['amount']
    transaction = Transaction.objects.get(id = trans_id)
    transaction.sent_amount = amount
    transaction.is_validated = True
    if transaction.order:
        transaction.order.update_order()
        transaction.order.save()
    transaction.save()
    return redirect('manager_dashboard')


@login_required
def refresh_order(request):
    if not request.user.is_admin:
        return redirect('profile')
    
    order_id = request.POST['order_id']
    order = Order.objects.get(id = order_id)
    order.update_order()
    order.save()
    return redirect('manager_dashboard')