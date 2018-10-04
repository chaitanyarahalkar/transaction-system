from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .models import Transaction,User,Bank
from django.db import transaction,IntegrityError
from django.contrib import messages
import time 
import random
import string  
from django.views.decorators.http import require_POST
from django.db import IntegrityError

# Create your views here.
def index(request):
	return render(request,'app/index.html')

@transaction.atomic
def createaccount(user):
	try:
		account = Bank()
		account.account_number = ''.join(random.choices(string.digits, k=20))
		account.user = user
		account.save()
	except IntegrityError:
		createaccount()

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			createaccount(user)
			return render(request,'app/success.html')
	else:
		form = UserRegisterForm()

	return render(request,'app/signup.html',{'form':form})


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
	entry = User.objects.get(email=email)
	entry.email = email
	entry.address = address
	entry.city = city
	entry.save()
	messages.info(request, 'Your profile was updated.')
	return redirect('/user/')


@login_required
def user(request):
	return render(request,'app/user.html')



@login_required
def my_transaction(request):
	if request.method == 'POST':
		if user.is_active:
			request.session.set_expiry(300)
			if request.session.get_expiry_age() == 0:
				render(request,'app/expired.html')
			tx = Transaction()
			upi_id = request.POST.get("toid")
			try:
				with transaction.atomic():
					if int(upi_id) == request.user.upi:
						pass
			except IntegrityError:
				messages.error(request,'Error in transaction performing!')

			transaction.on_commit(send_message)

		
	return HttpResponse('<h3>done</h3>')

@login_required
def transactions(request):
	transactions = Transaction.objects.get(from_id=request.user.id)
	return render(request,'app/transactions.html')

@transaction.atomic
def updatebalance(request,amount):
	request.user.wallet_balance+=amount


@transaction.atomic
def getbalance(request):
	account = Bank.objects.get(user=request.user)
	return account

@transaction.atomic 
def updatebankbalance(account,amount):
	account.balance-=amount
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
						updatebankbalance(account,amount)
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


