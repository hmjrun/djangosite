from django.db import models

# Create your models here.
class Record_trade(models.Model):
	#订单号
	out_trade_no = models.CharField(max_length=200)
	#订单名称
	trade_subject = models.CharField(max_length=200)
	#订单说明
	trade_body = models.CharField(max_length=200)
	#订单总额
	trade_total_fee = models.CharField(max_length=200)
	#state 0=>fail 1=>success
	trade_state = models.IntegerField(default=0)

	def __str__(self):
		return self.trade_subject


class Goods(models.Model):
	# question = models.ForeignKey(Question,on_delete=models.CASCADE)
	goods_title = models.CharField(max_length=200)
	goods_subject = models.CharField(max_length=200)
	goods_price = models.CharField(max_length=200)


	def __str__(self):
		return self.goods_title