from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .models import Transaction,User
from django.db import transaction,IntegrityError
from django.contrib import messages
import time 
# Create your views here.
def index(request):
	return render(request,'app/index.html')

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
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

@login_required
def add_money(request):
	if request.method == 'POST':
		pin = request.POST.get("pin")
		amount = float(request.POST.get("amount"))
		try:
			with transaction.atomic():
				tx = Transaction()
				tx.from_id,tx.to_id = request.user.username,request.user.username
				tx.issuer_bank = "ICICI"
				if pin == request.user.upi_pin:
					#account = BankA.objects.get(bank_id=request.user.id)
					updatebalance(request,amount)
					tx.amount = amount
					tx.txn_id = int(time.time())
					request.user.save()
					tx.save()
					messages.info(request, 'Added {} to your wallet.'.format(amount))
				else:
					messages.warning(request,'Invalid PIN!')
		except IntegrityError:
			messages.error(request,'Error in transaction performing!')



	return redirect('/profile/')


