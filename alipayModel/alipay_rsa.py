#coding:utf-8

import cgi, base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import hashlib
import urllib
import time


'''
raw_data = 'partner="2088701924089318"&seller="774653@qq.com"&out_trade_no="123000"&subject="123456"&body="2010新款NIKE 耐克902第三代板鞋 耐克男女鞋 386201 白红"&total_fee="0.01"¬ify_url="http://notify.java.jpxx.org/index.jsp"'
sign_data = sign(raw_data)
print ("sign_data: %s"%sign_data)
print (verify(raw_data, sign_data))
'''
    #私钥文件
priKey = '''-----BEGIN RSA PRIVATE KEY-----
  MIIEogIBAAKCAQEAmJHsvCthyyTN0O4Np4SybXreeOH1qIZVLjj63HnyAL9YZ0SJ
  ROKPV3k/BYnVw2xcJAQtryUq8zsaoavcuNvdIUoqQs18GGlcDCcVpbFUAgMa6nSF
  fph+TMusxhLfWk5Evcm9LBkRaNb1RHGeEwn802nkDW/KWDwCh/JUl/izWmk/aP9r
  Zs3++ItIBwVtgdgcBe7r6HNCDL761lh91wkPwdJtQgS1NE6OArQlhcUVIBr56wTI
  jXj1ijHLiDC3ie3Hhz5ylz/f3SxmR0vKgkLcAN+6OuIh5IAjpoZb9MJeTRO39sAb
  XbIb5mV7uYvpi5icHDt38gXTceuPZvkm6RZ68QIDAQABAoIBAFxzqLHJ1APGdJWT
  e2C0j266Es/LlRIe/MT6sEEkABql2IsTQ98jLttB1Ielo4w9QIRup8RHUIR9n0Cy
  pRi72n7Os1cxr24Xgji3Am4aS57AhPHn0/EHtRkSHssUKpZNcWhUNDbhpeQSxiNI
  ehJtbfAqbZAa2tGm452/obVJdl1lE/wF7KiOap/7DijnOaci3iJhSg9xinN1GtjU
  pvD4I1hydSF23Ls47J9M/QhPnLa3FidRwwrxJDLIZf/0qh9gIfaxRpa3yZsVG+sP
  PGCrrxS10W3ek5hu28OGhr7TO9sttO14bjPkAyBe+dusDy91D3qw9+uddXbM7uv/
  pJBSmnUCgYEAyjgsSFSjzXhvqT6Zjfo5GdoG9jSj77J03w2wXaWtQppGdAdpRHVe
  YE439wYkLfocv4y3dBrkCbltaJQyOujQ25qF9tAgX6t/BPR7F6mxYxdIqdw9HCAD
  GpcDpSgfNgqY+2Bx6FAsveP+ZtESWEiLIjbQpACpq9NqaR1xxsn9AMMCgYEAwSVw
  9m8bPKS33RRp7D1MhuXy2eHQGI48eqxNi2PVDaiJnEmRqQIY87uASSbg+n95i69q
  cfx46Un/eWp/aU9GspLR1bWjbXs+ZSHURFuZzxVatpacZqD8aXzTA2XdaFvKTVSD
  QRJDlu1kx2Tp8iOqDLEaYzuXssKEYyqDIvxGmjsCgYAy7jbo+LhQtbaZz7Ro986N
  3kXGmLd5VV7uFsqGq4WZsrVv37X5kf31D3407w0Jr2ayL8S8r1EjydnubvS/tYd0
  59Q5t22P6ueQ3epqqUiOBn08msWhYcamWcaHQDWsLLsfBMlrk1XRdazLRHj0V0ED
  mv6tb6VMK3EvjETtpk3cdQKBgDECxTVjYC/1REqvQWmW7HJWq1cqe9mfTi16x3qV
  bJy4paKo8HNIevhuHdFyMiiebENL0eD2xd+8zT0MDySz3ya1JtXp73x6h4y2Ftz5
  uX/Y1Vn7wdgxBZvm9syn7pTqpd0VkvDSJ6CGwMnwC4VME3yA/Ect+gJ8ZYecZAZe
  qbO9AoGADU4cOzon1iR/Dtluec6e4cBFa9PssVuhAKVGXHjfoopX6U4/zrR3K1+R
  OtAmBeQVqXeuI7sd/7eDoI41FkfM3bIxgIq256EcJF6ZSYYi9lhISNWieEft/bN4
  UjTLRc/D8LQtvyE7fCyH3bKFlH3aabrPteDSlgpDdqqHaWMmEBU=
  -----END RSA PRIVATE KEY-----'''

  #公钥文件
pubKey = '''-----BEGIN PUBLIC KEY-----
  MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmJHsvCthyyTN0O4Np4Sy
  bXreeOH1qIZVLjj63HnyAL9YZ0SJROKPV3k/BYnVw2xcJAQtryUq8zsaoavcuNvd
  IUoqQs18GGlcDCcVpbFUAgMa6nSFfph+TMusxhLfWk5Evcm9LBkRaNb1RHGeEwn8
  02nkDW/KWDwCh/JUl/izWmk/aP9rZs3++ItIBwVtgdgcBe7r6HNCDL761lh91wkP
  wdJtQgS1NE6OArQlhcUVIBr56wTIjXj1ijHLiDC3ie3Hhz5ylz/f3SxmR0vKgkLc
  AN+6OuIh5IAjpoZb9MJeTRO39sAbXbIb5mV7uYvpi5icHDt38gXTceuPZvkm6RZ6
  8QIDAQAB
  -----END PUBLIC KEY-----'''

  #alipay_pub_key
alipay_pub_key = '''MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDI6d
  306Q8fIfCOaTXyiUeJHkrIvYISRcc73s3vF1ZT7XN8RNPwJxo8pWaJMmvyTn9N4
  HQ632qJBVHf8sxHi/fEsraprwCtzvzQETrNRwVxLO5jVmRGi60j8Ue1efIlzPXV
  9je9mkjzOmdssymZkh2QhUrCmZYI/FCEa3/cNMW0QIDAQAB'''
verfyURL={
    "https":"https://www.alipay.com/cooperate/gateway.do?service=notify_verify",
    "http" :"http://notify.alipay.com/trade/notify_query.do?",
    }
#gateway="https://www.alipay.com/cooperate/gateway.do"
#gateway="https://mapi.alipay.com/gateway.do"
gateway = "https://openapi.alipay.com/gateway.do"
class alipay_rsa:
    def __init__(self,
                 app_id="app_id",
                 notifyurl="异步通知回调URL",
                 returnurl="跳转回调URL"
                ):
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            self.conf={
              'app_id'          :   app_id,
              'method'          :  "alipay.trade.wap.pay",
              'payment_type'    :   "1",
              'charset'         :   "utf-8", 
              'sign_type'       :   "RSA",
              'version'         :   "1.0",
              'timestamp'       :   timestamp,
              'notify_url'      :   notifyurl,
              'return_url'      :   returnurl,   
              #其他参数，如果有默认值定义在下面：

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

        self.conf['biz_content'] = params

        #筛选,排序,组成待签名字符串
        wait_sign_str = self.populateURLStr(self.conf)
        print ("wait_sign_str: " + wait_sign_str)

        #签名RSA
        sign=self.sign_rsa(wait_sign_str)

        self.conf['sign']=sign
        
        rlt=''
        for k in self.conf:
            if self.conf[k]==None or len(self.conf[k])==0:
                continue
            rlt=rlt+"&%s=%s"%(k,self.conf[k])
        full_url = gateway + "?" + rlt
        print ("full_url: " + full_url)
        return full_url

    def sign_rsa(self, data):
      key = RSA.importKey(priKey)
      h = SHA.new(data.encode('utf-8'))
      signer = PKCS1_v1_5.new(key)
      signature = signer.sign(h)
      return base64.b64encode(signature)




    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    '''
    *RSA签名
  	* data待签名数据
  	* 签名用商户私钥，必须是没有经过pkcs8转换的私钥
  	* 最后的签名，需要用base64编码
  	* return Sign签名
  

  	def sign_rsa(self, data):
    	key = RSA.importKey(priKey)
    	h = SHA.new(data.encode('utf-8'))
    	signer = PKCS1_v1_5.new(key)
    	signature = signer.sign(h)
    	return base64.b64encode(signature)

    *RSA验签
  	* data待签名数据
  	* signature需要验签的签名
  	* 验签用支付宝公钥
  	* return 验签是否通过 bool值
  	
  	def verify(self, data, signature):
    		key = RSA.importKey(pubKey)
    		h = SHA.new(data.encode('utf-8'))
    		verifier = PKCS1_v1_5.new(key)
    		if verifier.verify(h, base64.b64decode(signature)):
    			return True
    		return False
    '''