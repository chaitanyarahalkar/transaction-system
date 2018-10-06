from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .models import Transaction,User,Bank,OTP 
from django.db import transaction,IntegrityError
from django.contrib import messages
import time 
import random
import string  
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import csv
from django_otp.util import random_hex
from .otp import TOTPVerification
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import views as auth_views

banks = ['ICICI','HSBC','HDFC','Barclays','Punjab National','Bank of Baroda','Bank of Maharashtra','Axis']

# Create your views here.
def index(request):
	return render(request,'app/index.html')

@transaction.atomic
def setbool(request):
	ob = OTP.objects.get(user=request.user)
	ob.verified = True
	ob.save()

def otpcheck(user):
	return OTP.objects.get(user=user).verified

@transaction.atomic
def getiv(request):
	ob = OTP.objects.get(user=request.user)
	ob.save()
	return ob.iv

def sendotp(request):
	otp = TOTPVerification(key=getiv(request))
	print(otp.generate_token())
	return otp 

@login_required
def verifyotp(request):
	otp_obj = sendotp(request)
	init_req = request
	if request.method == 'POST':
		setbool(init_req)
		otp = request.POST.get("otp")
		if otp_obj.verify_token(int(otp)):
			return redirect('/profile/')
		else:
			messages.error(request, 'Invalid OTP!')
	return render(request,'app/otp.html')


@transaction.atomic
def createaccount(user):
	try:
		account = Bank()
		account.account_number = ''.join(random.choices(string.digits, k=20))
		account.user = user
		account.bank = random.choice(banks)
		account.save()
	except IntegrityError:
		createaccount(user)

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			iv = random_hex(20)
			user = form.save()
			otp = OTP(iv=iv,user=user)
			otp.save()
			createaccount(user)
			return render(request,'app/success.html')
	else:
		form = UserRegisterForm()

	return render(request,'app/signup.html',{'form':form})

@user_passes_test(otpcheck,login_url='/login')
@login_required
def profile(request):
	if request.user.is_authenticated:
		if request.user.is_active:
			request.session.set_expiry(10000)
	return render(request, 'app/dashboard.html')

@require_POST
@login_required
def update(request):
	email = request.POST.get("email") 
	address = request.POST.get("address")
	city = request.POST.get("city")
	fname = request.POST.get("fname")
	lname = request.POST.get("lname")
	entry = User.objects.get(email=email)
	entry.email = email
	entry.address = address
	entry.city = city
	entry.first_name = fname 
	entry.last_name = lname
	entry.save()
	messages.info(request, 'Your profile was updated.')
	return redirect('/user/')


@login_required
def user(request):
	return render(request,'app/user.html')


@login_required
def transactions(request):
	transactions = Transaction.objects.filter(from_id=request.user.username)
	return render(request,'app/transactions.html',{'transactions':transactions})

@transaction.atomic
def updatebalance(request,amount):
	request.user.wallet_balance+=amount


@transaction.atomic
def getbalance(request):
	account = Bank.objects.get(user=request.user)
	return account

@transaction.atomic 
def updatebankbalance(account,amount,sign):
	if sign == "-":
		account.balance-=amount
	elif sign == "+":
		account.balance+=amount
	
	account.save()


@require_POST
@login_required
def add_money(request):
	if request.method == 'POST':
		pin = request.POST.get("pin")
		amount = float(request.POST.get("amount"))

		try:
			with transaction.atomic():
				tx = Transaction()
				tx.from_id,tx.to_id = request.user.username,request.user.username
				account = getbalance(request)
				balance,tx.issuer_bank = account.balance,account.bank
				if balance > amount:
					if pin == request.user.upi_pin:
						updatebalance(request,amount)
						updatebankbalance(account,amount,"-")
						tx.amount = amount
						tx.txn_id = int(time.time())
						request.user.save()
						tx.save()
						messages.info(request, 'Added {} to your wallet.'.format(amount))
					else:
						messages.warning(request,'Invalid PIN!')
				else:
					messages.warning(request,'Insufficient balance in your bank account!')

					
		except IntegrityError:
			messages.error(request,'Error in transaction performing!')



	return redirect('/profile/')

@transaction.atomic
def queryuser(username):
	try:
		user = User.objects.get(username=username)
		return Bank.objects.get(user=user)
	except ObjectDoesNotExist:
		return None 

	


@login_required
def money_transfer(request):
	if request.method == 'POST':
		amount = float(request.POST.get("amount"))
		pin = request.POST.get("pin")
		tx = Transaction()
		tx.from_id = request.user.username 
		tx.to_id = request.POST.get("id")
		tx.amount = amount
		try:
			account = getbalance(request)
			balance,tx.issuer_bank = account.balance,account.bank 
			recv_account = queryuser(tx.to_id)
			if recv_account is not None:
				if balance > amount:
					if pin == request.user.upi_pin:
						updatebankbalance(account,amount,"-")
						updatebankbalance(recv_account,amount,"+")
						tx.txn_id = int(time.time())
						tx.save()
						messages.info(request,'Transferred {} to {} '.format(amount,tx.to_id))
					else:
						messages.warning(request,'Invalid PIN!')
				else:
					messages.warning(request,'Insufficient balance!')
			else:
				messages.warning(request,'Invalid ID!')
		except IntegrityError:
			messages.error(request,'Error in performing transaction!')

	return redirect('/profile/')






@login_required
def invoice(request):
	transactions = Transaction.objects.filter(from_id=request.user.username)
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="invoice.csv"'

	writer = csv.writer(response)
	writer.writerow(['ID', 'To ID', 'Issuer Bank', 'Amount','Paid On'])
	for t in transactions:
		writer.writerow([t.txn_id,t.to_id,t.issuer_bank,t.amount,t.paid_on])

	return response

@login_required
def logout(request):
	ob = OTP.objects.get(user=request.user)
	ob.verified = False
	ob.save()
	return auth_views.LogoutView.as_view(template_name='app/logout.html')(request)
