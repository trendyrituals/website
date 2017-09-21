from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)
from .models import Course, Coin
from .forms import CourseForm

# user landing page on desk
def home(request):
	if request.user.is_authenticated():
		user = request.user
		persent = Coin.objects.filter(user_name=user)
		if persent:
			email = request.user.email
			course_count = Course.objects.filter(user_name=request.user).count()
			total_coin = Coin.objects.get(user_name=request.user)
			value = total_coin.coin
			csr_list_first = Course.objects.filter().exclude(user_name=request.user).order_by('-timestamp')

			paginator = Paginator(csr_list_first, 10) # Show 25 contacts per page

			page = request.GET.get('page')
			try:
				csr_list = paginator.page(page)
			except PageNotAnInteger:
			# If page is not an integer, deliver first page.
				csr_list = paginator.page(1)
			except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
				csr_list = paginator.page(paginator.num_pages)

			context = {
			"user": user,
			"email": email,
			"course_count": course_count,
			"coin": value,
			"courses": csr_list
			}
			return render(request,"user_dash.html", context)
		if not persent:
			return render(request,"first_user_dash.html",)



#search course by subject, content, topics, lesson name, course id 
def search_course(request):
	if request.user.is_authenticated():
		query = request.GET.get("q")
		if query:
			queryset_list = Course.objects.filter(
				Q(course_name__icontains=query) |
				Q(description__icontains=query) |
				Q(subject__icontains=query) |
				Q(pk__icontains=query) 
				).distinct().exclude(user_name=request.user).order_by('-timestamp')
			paginator = Paginator(queryset_list, 10) # Show 25 contacts per page

			page = request.GET.get('page')
			try:
				queryset = paginator.page(page)
			except PageNotAnInteger:
			# If page is not an integer, deliver first page.
				queryset = paginator.page(1)
			except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
				queryset = paginator.page(paginator.num_pages)

			context = {
				"object_list":queryset
			}
			return render(request,"search_course.html", context)
		return render(request,"search_course.html")


#course posted by user himself
def user_course(request):
	if request.user.is_authenticated():
		course_list = Course.objects.filter(user_name = request.user).order_by("-id")
		context = {
		"object_list": course_list
		}
		return render(request,"user_course.html", context)




# user added course view or function 
def add_course(request):
	if request.user.is_authenticated():
		form = CourseForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			new_course = form.save(commit=False)
			new_course.user_name = request.user
			new_course.save()
			get_coin = Coin.objects.get(user_name=request.user)
			coin_usr = get_coin.coin+1
			get_coin.coin = coin_usr
			get_coin.save()
			form = CourseForm()
			txt = "New course added by you. You got 1 coin."
			messages.success (request, txt, extra_tags= 'text-success')
		context = {
		"form": form
		}
		return render(request,"add_course.html", context)




#user's course view. the course is add by user himself 
def user_course_view(request, id=None):
	if request.user.is_authenticated():
		instance = get_object_or_404(Course, id=id)
		context = {
			"title" : instance.course_name,
			"instance": instance,
			"subject" : instance.subject,
			"description" : instance.description,
		}
		return render(request, "course_view.html", context)




#new user coin table create and redirect to the home page of user dashboard
def ready_user(request, username=None):
	if request.user.is_authenticated():
		new_entry = Coin.objects.create(user_name = username, coin=8)
		new_entry.save()
		return redirect("/desk/")




# get coins page where user is able to purchase more coins 
def coins(request):
	if request.user.is_authenticated():
		return render(request,"coin.html")



def cost_view(request, id=None):
	if request.user.is_authenticated():
		user_coin = Coin.objects.get(user_name=request.user)
		coins = user_coin.coin
		if coins>=2:
			instance = get_object_or_404(Course, id=id)
			get_coin = Coin.objects.get(user_name=request.user)
			coin_usr = get_coin.coin-2
			get_coin.coin = coin_usr
			get_coin.save()
			context = {
				"title" : instance.course_name,
				"instance": instance,
				"subject" : instance.subject,
				"description" : instance.description,
			}
			return render(request,"cost_view.html",context)
		if coins<2:
			context = {
			"msg" :"Sorry",
			"little_msg" :"You dont have enough coins"
			}
			return render(request,"sorry_msg.html", context)


#delete course by user 
def delete_course(request,id=None):
	if request.user.is_authenticated():
		instance = get_object_or_404(Course, id=id)
		instance.delete()
		txt = "Course deleted by you."
		messages.success (request, txt, extra_tags= 'text-danger')
		return redirect("/desk/user_course/")

#successful payment and add coins
def pay_success(request):
	if request.user.is_authenticated():
		get_coin = Coin.objects.get(user_name=request.user)
		add_coin = get_coin.coin + 20
		get_coin.coin = add_coin
		get_coin.save()
		messages.success (request,"20 coins successfully added to your account.",extra_tags= 'text-success')
		return render(request,"success.html")

#when payment is unsuccessful . dont add coins to the user account
def pay_unsuccessful(request):
	if request.user.is_authenticated():
		messages.success (request, "Payment unsuccessful try again.", extra_tags= 'text-danger')
		return render(request,"unsuccessful.html")


#and the last user logout function 
def logout_view(request):
	if request.user.is_authenticated():
		logout(request)
		return redirect("/")