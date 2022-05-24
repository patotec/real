from django.shortcuts import redirect, render,get_list_or_404, get_object_or_404,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .models import *
# from index.forms import 
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
import threading

User = get_user_model()



class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('acc/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMultiAlternatives(subject=email_subject, body=email_body, from_email=settings.EMAIL_HOST_USER,to=[user.email] )
    email.attach_alternative(email_body, "text/html")

    EmailThread(email).start()


@login_required(login_url='/user/login/')
def profile(request):
    qs = Pay_method.objects.filter(visible=True)
    context = {'wal':qs}
    return render(request, 'acc/profile.html',context)



def fund(request):
    qs = Pay_method.objects.filter(visible=True)
    context = {'wal':qs}
    return render(request, 'acc/deposit.html',context)

def myfund(request,slug):
    post = get_object_or_404(Pay_method, slug=slug)
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        wallet = request.POST.get('wallet')
        image = request.FILES.get('image')
        user = request.POST.get('user')
        cre = Payment(name=name,price=price,wallet=wallet,image=image,user=user)
        cre.save()
        messages.success(request,'Your Payment will be Aproved in the next 24hrs...')
    context = {'data':post}
    return render(request,'acc/payment-method.html',context)

# def help(request):
#     if request.method == 'POST':
#         form = Contactform(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Thanks for your message we will repyl you shortly')
#     else:
#         form = Contactform()
#     return render(request, 'acc/help.html')

def signupView(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        image = request.FILES.get('image')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('userurl:signup')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('userurl:signup')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email Already Taken')
            return redirect('userurl:signup')
        else:
            user = User.objects.create_user(username=username, password=password1,fullname=fullname,email=email,phone=phone,country=country,image=image)
            send_activation_email(user, request)
            messages.add_message(request, messages.SUCCESS,'We sent you an email to verify your account')
            return redirect('userurl:login')
    return render(request, 'acc/register.html')


def loginView(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			newurl = request.GET.get('next')
			if newurl:
				return redirect(newurl)
			return redirect('userurl:profile')
		else:
			messages.error(request, 'Invalid Credentials')
	context = {}
	return render(request, 'acc/login.html')

def logout_view(request):
	logout(request)
	return redirect('/user/login')


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordCodeForm(request.POST)
        if form.is_valid():
			# try:
            email = form.cleaned_data.get('user_email')
            detail = ChangePasswordCode.objects.filter(user_email=email)
            if detail.exists():
				# messages.add_message(request, messages.INFO, 'invalid')
                for i in detail:
                    i.delete()
                form.save()
                test = ChangePasswordCode.objects.get(user_email=email)
                subject = "Change Password"
                from_email = settings.EMAIL_HOST_USER
                # Now we get the list of emails in a list form.
                to_email = [email]
                #Opening a file in python, with closes the file when its done running
                detail2 = "https://Clickingcoins.com.com/user/"+ str(test.user_id)
                msg = EmailMessage(
                'Reset Password',
                'Click ' + detail2 + " To reset your password",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                )
                msg.send()
                return redirect('userurl:change_password_confirm')
            else:
                form.save()
                test = ChangePasswordCode.objects.get(user_email=email)
                html = "https://Clickingcoins.com.com/user/"+ str(test.user_id)

                msg = EmailMessage(
                'Reset Password',
                'Click ' + html + " To reset your password",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                )
                msg.send()
                return redirect('userurl:change_password_confirm')

        else:
            return HttpResponse('Invalid Email Address')
    else:
        form = ChangePasswordCodeForm()
    return render(request, 'acc/change_password.html', {'form':form})


def change_password_confirm(request):
	return render(request, 'acc/change_password_confirm.html', {})
def change_password_code(request, pk):
	try:
		test = ChangePasswordCode.objects.get(pk=pk)
		detail_email = test.user_email
		u = User.objects.get(email=detail_email)
		if request.method == 'POST':
			form = ChangePasswordForm(request.POST)
			if form.is_valid():
				u = User.objects.get(email=detail_email)
				new_password = form.cleaned_data.get('new_password')
				confirm_new_password = form.cleaned_data.get('confirm_new_password')
				if new_password == confirm_new_password:
					u.set_password(confirm_new_password)
					u.save()
					test.delete()
					return redirect('userurl:change_password_success')
				else:
					return HttpResponse('your new password should match with the confirm password')


			else:
				return HttpResponse('Invalid Details')
		else:
			form = ChangePasswordForm()
		return render(request, 'acc/change_password_code.html', {'test':test, 'form':form, 'u':u})
	except ChangePasswordCode.DoesNotExist:
		return HttpResponse('bad request')


def change_password_success(request):
	return render(request, 'acc/suc1.html', {})


def rev(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        cre = Request.objects.create(email=email,name=name,message=message)
    return render(request, 'acc/suc1.html', {})
