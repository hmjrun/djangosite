#!/usr/bin/env python
# encoding: utf-8
'''
Created on 2011-1-5
@author: codeback@gmail.com
'''
import hashlib
import urllib

verfyURL={
    "https":"https://www.alipay.com/cooperate/gateway.do?service=notify_verify",
    "http" :"http://notify.alipay.com/trade/notify_query.do?",
    }
#gateway="https://www.alipay.com/cooperate/gateway.do"
gateway="https://mapi.alipay.com/gateway.do"
#gateway = "https://openapi.alipay.com/gateway.do"
class alipay:
    def __init__(self,
                 partner="您的淘宝身份",
                 #app_id="app_id",
                 key="您的淘宝Key",
                 sellermail="卖家邮箱",
                 notifyurl="异步通知回调URL",
                 returnurl="跳转回调URL",
                 showurl="产品页面"):
            
            self.key=key;
            self.conf={
              'partner'         :   partner,
              'seller_id'       :   partner,
              'service'         :   "alipay.wap.create.direct.pay.by.user",
              'payment_type'    :   "1",
              'notify_url'      :   notifyurl,
              'return_url'      :   returnurl,
              'show_url'        :   showurl,
              '_input_charset'  :   "utf-8", 
              'sign_type'       :   "MD5",        
              #其他参数，如果有默认值定义在下面：
              'paymethod'       :   "",
              'mainname'        :   "",
              }



    def populateURLStr(self,params):
        ks=params.keys()
        ks = sorted(ks)

        rlt=''
        for k in ks:
            if params[k]==None or len(params[k])==0 \
                or k=="sign" or k=="sign_type" or k=="key":
                continue
            rlt=rlt+"&%s=%s"%(k,params[k])
        url = "URL:"+rlt[1:]
        print(url)
        return rlt[1:]
        

    def buildSign(self,params):
        sign=hashlib.md5((self.populateURLStr(params)+self.key).encode('utf-8')).hexdigest()
        print ("md5 sign is %s" % sign)
        return sign
    
    
    '''
      校验支付宝返回的参数，交易成功的通知回调.
      校验分为两个步骤：检查签名是否正确、访问支付宝确认当前数据是由支付宝返回。
      
      params为支付宝传回的数据。
    '''
    def notifiyCall(self,params,verify=True,transport="http"):
        sign=None
        if params.has_key('sign'):
            sign=params['sign']
        locSign=self.buildSign(params)
        
        if sign==None or locSign!=sign:
            print ("sign error.")
            return "fail"
        
        if params['trade_status']!='TRADE_FINISHED' and  params['trade_status']!='TRADE_SUCCESS':
            return "fail"
        
        if not verify:
            return "success"
        else:
            print ("Verify the request is call by alipay.com....")
            url = verfyURL[transport] + "&partner=%s&notify_id=%s"%(self.conf['partner'],params['notify_id'])
            response=urllib2.urlopen(url)
            html=response.read()
       
            print ("aliypay.com return: %s" % html)
            if html=='true':
                return "success"
            
            return "fail"

    '''
        生成提交到支付宝的表单，用户通过此表单将订单信息提交到支付宝。
        
        由params参数提供订单信息，必须包含以下几项内容：
        out_trade_no：订单号
        subject     :订单名称、或商品名称
        body        :订单备注、描述
        total_fee   :总额
    '''
    def createPayForm(self,params,method="POST",title="确认，支付宝付款"):
        #Python 字典(Dictionary) update() 函数把字典dict2的键/值对更新到dict里。
        params.update(self.conf)

        sign=self.buildSign(params)
        params['sign']=sign
        
        ele=""
        ks = params.keys()
        ks = sorted(ks)
        for k in ks:
          print ("key in params : %s"%k)
          if params[k]==None or len(params[k])==0 :
            continue
          ele = ele + " <input type='hidden' name='%s' value='%s' />" % (k,params[k])
          html='''
            <form name='alipaysubmit' action='%s?_input_charset=%s' method='%s' target='_blank'>
                %s
                <input type="submit" value="%s" />
            </form>
            ''' % (gateway,params['_input_charset'],method,ele,title)
            
        return html
