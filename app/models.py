from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.contrib import admin 
from django.contrib.auth.models import AbstractUser
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Max,Count,Avg
from django.contrib import messages
from import_export.admin import ImportExportActionModelAdmin
import uuid
# Create your models here.


class Transaction(models.Model):
	paid_on = models.DateTimeField()
	from_id = models.CharField(max_length=20)
	to_id = models.CharField(max_length=20)
	txn_id = models.CharField(max_length=20)
	upi_id = models.BigAutoField(primary_key=True)
	issuer_bank = models.CharField(max_length=20)
	amount = models.FloatField(default=0)

	def __str__(self):
		return self.txn_id


class User(AbstractUser):
	email = models.EmailField()
	address = models.CharField(max_length=50)
	contact = models.IntegerField(default=0)
	city = models.CharField(max_length=12)
	upi_pin = models.CharField(max_length=4)
	wallet_balance = models.FloatField(default=0.000)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')


	def __str__(self):
		return self.username

class TransactionAdmin(admin.ModelAdmin):
	list_display = ('paid_on','from_id','to_id','txn_id','upi_id','issuer_bank','amount')
	empty_value_display = '-empty-'
	list_filter = ('paid_on','issuer_bank')
	#readonly_fields = ('paid_on','from_id','to_id','txn_id','upi_id','issuer_bank','amount')
	search_fields = ['from_id','to_id']
	actions = ['export_as_json','maximum','average']
	change_list_template = 'change_list_graph.html'
	save_as = True
	save_on_top = True 

	def export_as_json(TransactionAdmin,request,queryset):
		response = HttpResponse(content_type="application/json")
		serializers.serialize("json",queryset,stream=response)
		return response

	def maximum(self,request,queryset):
		max_tx = Transaction.objects.all().aggregate(Max('amount'))
		self.message_user(request,'{} is the maximum of all transaction amounts'.format(max_tx['amount__max']),level=messages.INFO)

	def average(self,request,queryset):
		avg_tx = Transaction.objects.all().aggregate(Avg('amount'))
		self.message_user(request,'{} is the average of all transaction amounts'.format(avg_tx['amount__avg']),level=messages.INFO)


class UserAdmin(ImportExportActionModelAdmin):
	list_display = ('username','email','address','contact','city','upi_pin','is_staff')
	empty_value_display = '-empty-'
	list_filter = ('city',)
	readonly_fields = ('upi_pin','email','username')
	search_fields = ['username','email','contact']



