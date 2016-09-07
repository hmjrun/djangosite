from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Goods,Record_trade
import uuid
from . import alipay
# Create your views here.
alipayTool=alipay.alipay(  
				#支付宝身份ID
                partner="2088121136801926",  
                #支付宝生成的key
                key="j57lno9gjeegqu3vazgwred8689vuazi",  
                #商家支付宝帐号（邮箱）
                sellermail="zhangshuo@hanyunhk.cn",  
                notifyurl="http://www.mjcode.cn:8080/alipayModel/notifyUrl",  
                returnurl="http://www.mjcode.cn:8080/alipayModel/returnUrl",  
                showurl="http://www.mjcode.cn"  
                )

def index(request):
    
    latest_goods_list = Goods.objects.all()[:5]

    context = {
    	'latest_goods_list':latest_goods_list,
    }
    
    return render(request,'alipayModel/index.html',context)

def buy(request,goods_id):
	goods = get_object_or_404(Goods,pk=goods_id)

	trade_no = str(uuid.uuid1())
	params = {
		'out_trade_no' : trade_no,
		'subject' : goods.goods_subject,
		'body' : 'this is Test buy use alipay',
		'total_fee' : goods.goods_price
	}

	r = Record_trade.objects.create(
		out_trade_no=params['out_trade_no'],
		trade_subject=params['subject'],
		trade_body=params['body'],
		trade_total_fee=params['total_fee'])

	payhtml = alipayTool.createPayForm(params)

	return HttpResponse(payhtml) 

def notifyUrl(request):
	rlt=alipayTool.notifiyCall(f,verify=True)  
	#依据支付宝的要求，此URL返回的值为success或fail  
	#因此，当rlt为success时（即支付成功），做相应的处理  
	#然后，直接将rlt写到输出流。  
	  
	if rlt=='success':  
	     #paySuccess(f['out_trade_no'])  
	     print (f['out_trade_no'])
	  
	return HttpResponse(rlt)

def returnUrl(request):
	#注意，与异步回处理相同，在跳转回调的处理上，仍是调用notifiyCall函数  
	#并且参数与返回完全一样。  
	  
	rlt=alipayTool.notifiyCall(f,verify=True)  
	  
	#只是验证后的处理不同，这里需要给用户显示一个页面。  
	if rlt=='success':  
	   print (f['out_trade_no'])  
	   #显示支付成功的页面  
	   return HttpResponse("ok and this is redirURl")
	else:  
	   #显示未能成功支付的页面  
	  return HttpResponse("fail and this is redirURl") 