from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from course.models import Course, Subscription, Unit
from payment.models import Number, Order, Transaction
from django.contrib import messages

# Create your views here.

@login_required
def payment(request):
    courses = Course.objects.filter(released = True).exclude(subscription__user = request.user, subscription__active = True)

    details = {}
    for course in courses:
        details[course.course_name] = {
            'price': course.course_price,
            'id': course.id,
            'units': []
        }
        for unit in course.unit_set.all().exclude(subscription__user = request.user, subscription__active = True):
            details[course.course_name]['units'].append(unit)
    
    number = Number.objects.all()[0]
    context = {
        'details' : details,
        'number': number,
    }

    return render(request, 'payment/payment.html', context = context)


@login_required
def authorize_payment(request):
    units = request.POST.getlist('units[]')
    sender_number = request.POST['sender_number']
    trxID = request.POST['trxid']

    # Creating transaction object
    transaction = Transaction(sender_number = sender_number, trxID = trxID)
    transaction.save()

    # Creating Order, (if applicable)
    if len(units) > 0:
        order = Order(user = request.user)
        order.save()
        transaction.order = order
        transaction.save()
    
        ## Creating subscriptions
        total_price = 0
        for unit in units:
            if unit[0] == '_':
                try:
                    course = Course.objects.get(id = unit[1:])
                    total_price += int(course.course_price)
                    subscription = Subscription(subscription_type = 0, course = course, order = order, user = request.user)
                    subscription.save()
                except:
                    pass
            else:
                try:
                    unitt = Unit.objects.get(id = unit)
                    total_price += int(unitt.unit_price)
                    subscription = Subscription(subscription_type = 1, unit = unitt, order = order, user = request.user)
                    subscription.save()
                except:
                    pass
        order.required_amount = total_price
        order.save()


    messages.success(request, 'Your payment is being processed. We will update your subscription withing 24 hours')                
    return redirect('profile')


@login_required
def user_payment_details(request, *args, **kwargs):
    payment_id = kwargs['payment_id']
    order = Order.objects.filter(id = payment_id)
    if order.count() > 0:
        order = order[0]
        if order.user.id != request.user.id:
            return redirect('profile')
        context = {
            'payment': order,
        }

        payment_history = Order.objects.filter(user = request.user)

        context['payments'] = payment_history

        return render(request, 'payment/user_payment_details.html', context = context)
        
    else:
        return redirect('profile')