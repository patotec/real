from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, request
from .models import *
from .forms import *
from django.contrib import messages
from user.models import *
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

User = get_user_model()

def myindex(request):
	fds = Team.objects.all()
	qs = Review.objects.all()
	pla = Place.objects.all()
	prop = Property.objects.filter().order_by('-created')
	context = {'inv':fds,'rev':qs,'prop':prop,'pla':pla}
	return render(request, 'index/index.html',context)


@login_required(login_url='/user/login/')
def myprop(request,slug):
	listing = get_object_or_404(Property, slug=slug)
	if request.method == 'POST':
		email = request.POST.get('email')
		message = request.POST.get('message')
		user = User.objects.get(username=request.user)
		cre = Request.objects.create(message=message,email=email,property=listing,user=user)
		email_body = render_to_string('index/re.html', {
		'user': user,
		'data':listing
		})
		msg = EmailMultiAlternatives(subject='Invoice', body=email_body, from_email=settings.DEFAULT_FROM_EMAIL,to=[cre.email] )
		msg.attach_alternative(email_body, "text/html")
		msg.send()
		return redirect('userurl:login')

	context = {
	'data': listing
	}
	return render(request, 'index/hg.html',context)


def myabout(request):
	fds = Team.objects.all()
	qs = Review.objects.all()
	context = {'inv':fds,'rev':qs}
	return render(request, 'index/about.html',context)

def mycontact(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		name = request.POST.get('name')
		subject = request.POST.get('subject')
		message = request.POST.get('message')
		cre = Contact.objects.create(email=email,name=name,subject=subject,message=message)
		msg = EmailMessage('support', cre.email  +  "wants ur help  " + cre.message ,
		settings.DEFAULT_FROM_EMAIL,['hanspilgaard01@gmail.com'],)
		msg.send()
		messages.success(request, 'Thanks for your message we will repyl you shortly')
	return render(request, 'index/contact-us.html')

