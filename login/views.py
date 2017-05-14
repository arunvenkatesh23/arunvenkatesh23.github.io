from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import UserForm, PersonalDetailsForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import User
# from django.conf import settings
# import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket
socket.getaddrinfo('127.0.0.1', 8000)


def home(request):
    return render(request, 'login/login_form.html')


def about_us(request):
    return render(request, 'login/about_us.html')


def services(request):
    return render(request, 'login/services.html')


def admin_login(request):
    return HttpResponseRedirect('/admin/login/?next=/admin/')


def registration(request):
    form = UserForm(request.POST or None, request.FILES)
    if form.is_valid():
        user = form.save(commit=False)
        email = request.POST['email']
        user.avatar = request.FILES['avatar']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            user.set_password(password)
            user.save()
            user = authenticate(email=email, password=password)
            if user is not None:
                user.is_active = False
                # os.mkdir(os.path.join(settings.MEDIA_ROOT, user.username))
                user.save()
                id = user.id
                email = user.email
                send_email(email, id)
                return render(request, 'login/thank_you.html')
            else:
                return render(request, 'login/registration_form.html')
        else:
            msg = 'Password and confirm password does not match. Please try again!'
            context = {
                "msg": msg,
                "form": form,
            }
            return render(request, 'login/registration_form.html', context)
    context = {
        "form": form,
    }
    return render(request, 'login/registration_form.html', context)


def activate(request):
    id = int(request.GET.get('id'))
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    return render(request, 'login/activation.html')


def send_email(toaddr, id):
    text = "Greetings!\nYou have successfully registered in Cloud\nPlease click the link below to activate your " \
           "account:\nhttp://127.0.0.1:8000/activation/?id=%s" % id
    part1 = MIMEText(text, 'plain')
    msg = MIMEMultipart('alternative')
    msg.attach(part1)
    subject = "Activate your account at Cloud"
    msg = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % ('teamcakeshop15@gmail.com', toaddr, subject, msg.as_string())
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login('teamcakeshop15@gmail.com', 'wtfsandy@210')
    server.sendmail('teamcakeshop15@gmail.com', [toaddr], msg)
    server.quit()


def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/app/folders/')
            else:
                msg = 'Your account has been disabled. Please contact the administrator for further details.'
                context = {
                    "msg": msg,
                }
                return render(request, 'login/login_form.html', context)
        else:
            msg1 = 'Username or Password does not match. Please try again!'
            context = {
                "msg": msg1,
            }
            return render(request, 'login/login_form.html', context)
    return render(request, 'login/login_form.html')


def logout_user(request):
    logout(request)
    return render(request, 'login/login_form.html')


def personal_details(request, user_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user = request.user
        dp = get_object_or_404(User, pk=user_id)
        context = {
            'avatar': dp,
            'user': user,
        }
        return render(request, 'login/personal_details.html', context)


def delete_account_page(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        return render(request, 'login/delete_account.html')


def delete_account(request, user_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user = get_object_or_404(User, pk=user_id)
        email = user.email
        account_delete_send_email(email)
        user.delete()
        return render(request, 'login/regret.html')


def account_delete_send_email(toaddr):
    text = "Greetings!\nYou have successfully deleted your Cloud Account\nIf your account is deleted without your " \
           "knowledge please contact our Support Team or Administrator for help.\nThank you for being a loyal user.\n" \
           "Regards\nCloud Support Team\nteamcakeshop15@gmail.com"
    part1 = MIMEText(text, 'plain')
    msg = MIMEMultipart('alternative')
    msg.attach(part1)
    subject = "Delete your account at Cloud"
    msg = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % ('teamcakeshop15@gmail.com', toaddr, subject, msg.as_string())
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login('teamcakeshop15@gmail.com', 'wtfsandy@210')
    server.sendmail('teamcakeshop15@gmail.com', [toaddr], msg)
    server.quit()


def personal_details_update(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user = request.user
        data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'address': user.address,
            'city': user.city,
            'state': user.state,
            'country': user.country,
            'mobile': user.mobile,
        }
        form = PersonalDetailsForm(request.POST or None, instance=request.user, initial=data)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/personal_details/')
            else:
                context = {
                    'form': form,
                }
                return render(request, 'login/personal_details_update.html', context)
        else:
            context = {
                'form': form,
            }
            return render(request, 'login/personal_details_update.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'login/change_password.html', {
        'form': form
    })
