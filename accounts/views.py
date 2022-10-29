from email import message
from genericpath import exists
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from course.models import Course, Subscription
from payment.models import Order
from .forms import RegistrationForm, UserForm, UserProfileForm, UserProfile
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            institute = form.cleaned_data['institute']

            username = email.split('@')[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)

            user.phone_number = phone_number
            user.institute = institute
            user.save()

            # User Activation
            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Account To Login!'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Registraion Successful')
            base_url = reverse('register')  
            query_string =  urlencode({'login': True, 'status': 'verification', 'email': email})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
    else:
        form = RegistrationForm()

    context = {
        'login': False,
        'form': form
    }

    if request.method == 'GET':
        if request.GET.get('login') is not None and request.GET['login'] == 'true':
            context['login'] = True

    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(request, email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Welcome, ' + user.username)
            return redirect('profile')
        
        else:
            messages.error(request, "Invalid Login Credentials")
            return redirect('login')

    return redirect('/accounts/register/?login=true')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Successfully Logged Out!')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        userprofile = UserProfile(user = user)
        userprofile.save()
        messages.success(request, 'Congratulations! Your account is Activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid Activation Link')
        return redirect('register')


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset Password Email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password.'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Email has been send to you, reset password!!')
            return redirect('login')

        else:
            messages.error(request, 'Account Does Not Exists..')
            return redirect('forgotpassword')
    
    return render(request, 'accounts/forgotpassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('resetpassword')
    else:
        messages.error(request, 'The link is expired')
        return redirect('login')

def resetpassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            try:
                user = Account.objects.get(pk=uid)
            except:
                messages.error(request, 'Please try again!')
                return redirect('forgotpassword')
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Successfully Changed')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('resetpassword')
    else:
        return render(request, 'accounts/resetpassword.html')


@login_required(login_url='login')
def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile Has Been Updated')
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile,
    }

    courses = Course.objects.filter(released = True)

    details = {}
    for course in courses:
        details[course.course_name] = {
            'course_object': course,
            'subscribed_units': [],
        }
        for unit in course.unit_set.filter(subscription__user = request.user, subscription__active = True):
            details[course.course_name]['subscribed_units'].append(unit)
    
    context['details'] = details


    payment_history = Order.objects.filter(user = request.user)

    context['payments'] = payment_history
    
    return render(request, 'accounts/profile.html', context=context)


@login_required(login_url='login')
def changepassword(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password Updated Successfully.')
                return redirect('login')
            else:
                messages.error(request, 'Wrong password entered')
                return redirect('changepassword')
        else:
            messages.error(request, 'Passwords did not match.')
            return redirect('changepassword')

    return render(request, 'accounts/changepassword.html')

from django.urls import reverse
from urllib.parse import urlencode

def bug_solver(request):
    return render(request, 'accounts/bug_solver.html')