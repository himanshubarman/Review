from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
from django.http import JsonResponse
from .models import User, Product, Review, ActivityLog, RatingEvaluationString
from .serializer import ProductSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q, Sum
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.


def check(request):
	return render(request,'login.html')


def user_login(request):
	if request.method == 'POST':
		username = request.POST['email']
		password = request.POST['password']
		print(username,"mine",password)
		if username and password:
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/search')
				else:
					return HttpResponse("You're account is disabled.")
			else:
				return render(request,'registration/login.html',{"Error":"Username or password is incorrect or please check the confirmation mail once"})
		else:
			return render(request,'registration/login.html',{"Error":"Please enter all the required fields"})
	return render(request,'login.html')



@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/login')



def sign_up(request):
	first_name = request.POST.get("first-name", False)
	last_name = request.POST.get("last-name", False)
	email = request.POST.get("email", False)
	password = request.POST.get("password", False)
	email_check = User.objects.filter(email=email).exists()
	if email_check:
		return HttpResponse("email already exists")
	else:
		if email and password and first_name and last_name:
			User_register = User.objects.create(email=email,password=make_password(password),first_name=first_name,last_name=last_name,username=email)
			User_register.save()
			return HttpResponseRedirect('/login')
	return render(request,'signup.html')

@login_required
def search(request):
	return render(request,'search.html')

@login_required
def search_result(request):
	user = request.user
	text = request.GET.get("text", False)
	qs = list(Product.objects.filter().values())
	for i in qs:
		i["count"] = len(qs)
	return JsonResponse({'status':'True','data':qs}, status=200)

@login_required
def review(request,pk):
	print(request.user,"user-id",pk)
	qs = Product.objects.filter(id=pk).values()
	return render(request,'review.html',{"Data":qs})

@login_required
def review_submission(request):
	user = request.user
	if user.id:
		msg = request.POST.get("text", False)
		rating = request.POST.get("rating", False)
		product_id = request.POST.get("product_id", False)
		review_submit = Review.objects.create(product_item_id=product_id,sender_id=user.id,comment=msg,rating=rating)
		review_submit.save()
		reviews_log = ActivityLog.objects.create(product_item_id=product_id,user_id=user.id)
		reviews_log.save()
		return JsonResponse({"msg":"Review added successfully"})


class evaluation_of_review(APIView):
	permission_classes = []
	authentication_classes = []

	# authentication_classes = (TokenAuthentication,)
	# permission_classes = (IsAuthenticated,)

	def get(self,request):
		review_list = [0,1,2,3,4,5]
		result_count = {}
		string_list = []
		unformatted_list = []
		product_count = Product.objects.filter().values().count()
		review_count = Review.objects.filter(calculated_review=False).values().count()
		if product_count > 0 and review_count > settings.UNEVALUATED_REVIEWS:
			for i in review_list:
				if Review.objects.filter(rating=i,calculated_review=False).exists():
					count_qs = Review.objects.filter(rating=i,calculated_review=False).annotate(Count('rating'))
					result = count_qs.aggregate(Sum('rating__count'))
					result_count[i] = result['rating__count__sum']
					if result_count[i] > 0:
						unformatted_list.append(str(result_count[i]))
						string_list.append("("+str(result_count[i])+")")
				else:
					unformatted_list.append(str(0))
					string_list.append(str(0))
					result_count[i] = 0
			if string_list and unformatted_list:
				product_id_list = []
				qs = Review.objects.filter(calculated_review=False).values()
				for i in qs:
					product_id_list.append(i["product_item_id"])

				unique_product_list = list(set(product_id_list))
				for i in unique_product_list:
					save_format_string = RatingEvaluationString.objects.create(product_item_id=i,string_review="".join(unformatted_list),fromat_string_review="".join(string_list))
					save_format_string.save()
				qs.update(calculated_review=True)
				result_count["rating_result"] = "".join(unformatted_list)
				result_count["formatted_rating_result"] = "".join(string_list)
			return Response(result_count)
		else:
			result_count['error'] = "Mininmum requirement of review and product should be there for evaluation"
			return Response(result_count)



class activity_log(APIView):
	permission_classes = []
	authentication_classes = []


	def get(self,request):
		all_logs = {}
		all_logs['Review_logs'] = ActivityLog.objects.filter().values()
		all_logs['Review_string'] = RatingEvaluationString.objects.filter().values()
		return Response(all_logs)


class product_review(APIView):
	permission_classes = []
	authentication_classes = []

	def get(self,request,pk):
		print("value of pk",pk)
		result = {}
		result["product"] = Product.objects.filter(id=pk).values()
		result["review"] = RatingEvaluationString.objects.filter(product_item_id=pk).values()
		return Response(result)