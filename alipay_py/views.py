from django.http  import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from utils import get_request_json_body
#from common.hy_http import *
from . import alipay_config
from . import alipay_core
from django.utils import timezone

#构造一个支付请求
def make_payment_info(out_trade_no=None, subject=None, total_fee=None, body=None):

    order_info = {"partner": "%s" % (alipay_config.partner_id),
                   "service": "mobile.securitypay.pay",
                   "_input_charset": "utf-8",
                   "notify_url": "http://%s/callback" % (alipay_config.host),
                   #业务参数
                   "out_trade_no": None,
                   "paymnet_type": "1",
                   "subject": None,
                   "seller_id": alipay_config.alipay_account,
                   "total_fee": 0,
                   "body": None
    }

    order_info["out_trade_no"] = "%s" % (out_trade_no)
    order_info["subject"] = "%s" % (subject)
    if total_fee <= 0.0:
        total_fee = 0.01
    order_info["total_fee"] = total_fee
    order_info["body"] = "hsh_shop"
    return order_info

@csrf_exempt
def alipay(request, **kwargs):
	out_trade_no = 	timezone.datetime.now().strftime('%Y%m%d%H%M%S')
	subject 	= 	request.POST.get("subject","")
	total_fee 	=	request.POST.get("total_fee",0)
	body 		= 	request.POST.get("body","")
	payment_info =  make_payment_info(out_trade_no=out_trade_no,subject=subject,total_fee=total_fee,body=body)
	result = None
	try:
		result = alipay_core.make_payment_request(payment_info)
	except Exception as e:
		print (e)
	return JsonResponse({"status": "ok",'result':result})	

def callback(request, **kwargs):
    args = request.arguments
    for k, v in args.items():
        args[k] = v[0]

    check_sign = alipay_core.params_to_query(args)
    params = alipay_core.query_to_dict(check_sign)
    sign = params['sign']
    params = alipay_core.params_filter(params)
    message = alipay_core.params_to_query(params,quotes=False,reverse=False) #获取到要验证签名的串
    check_res = alipay_core.check_ali_sign(message,sign)  #验签

    if check_res == False:
        self.write("fail")
        return

    #这里是去访问支付宝来验证订单是否正常
    res = alipay_core.verify_from_gateway({"partner": alipay_config.partner_id, "notify_id": params["notify_id"]})
    if res == False:
        print ("fail")
        return

    trade_status = params["trade_status"]
    order_id = params["out_trade_no"]  #你自己构建订单时候的订单ID
    alipay_order = params["trade_no"]  #支付宝的订单号码
    total_fee = params["total_fee"]  #支付总额

    """
    下面是处理付款完成的逻辑
    """
    if trade_status == "TRADE_SUCCESS":  #交易成功
        #TODO:这里来做订单付款后的操作
        print ("success")
        return
    if trade_status == "TRADE_FINISHED":
        return

    if trade_status == "WAIT_BUYER_PAY":
        print ("success")
        return
    if trade_status == "TRADE_CLOSED":#退款会回调这里
        print ("success")