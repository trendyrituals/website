from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)

from .forms import UserLoginForm, UserRegisterForm


# Create your views here.

def index(request):
	return render(request,"home.html")





def login_view(request):
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect("/desk/")
	return render(request,"login.html", {"form":form})






def registration(request):
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)
		return redirect("/desk/")
	context = {
	"form": form
	}
	
	return render(request,"registration.html", context)




	

def about(request):
	return render(request,"about.html")

