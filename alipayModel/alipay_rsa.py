#coding:utf-8

import cgi, base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
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
MIICXgIBAAKBgQDJEKdiQyuOhXWsTGZCiLIJ0pqAhOLMiKIsZbMV0DGSNRbIADRTBM/SVP7PIWfoYgZjrMxoqKjfaOVx/nCMVLoqLpwSjp0BCWA92rFTxHhH4AfymlHSslvvmj5/sqfsssLY3gVuD/cLIR+ZTuehIHA8j7TMkldAUbSbXJyaVtIKWwIDAQABAoGAXRzXR0wwCaqImigvWzSOrrnXTxk7JtlHsSPP0ZQ+wKTRTgG6OZAK5i7yad3gjt+GcfZ+GyGwQvYC+82HNZWvODJUVFSut+Q6735DMm+kKPwubZfvA2VRVySYrVBSapAbU7nggV9PAJMa6ZuQZzfjFRHTrMuBpDeM/UOLOymjOVECQQD8cCcY9akZa1wjOYwg2dg2lqpiyr+V0l9B87y00WdTBXogyoXWTjszpwHiyAyyDwxPk/Gv5LMKsyngAL5mvYPvAkEAy+bu8W+RIo8kV6zQESZZ7j4idYk9Wc1taHAhEPh9SfYwa9kVzyPYU/FfpYgIBVy+Xw+1wsvDELVR1ZwoJgKEVQJBAOciMUozND9oA5blDB7QF53z2dJW3ZBqbHnQl8nfqgFkFGyNwnl0a9RhZ+KjVKx8BsOeLD7m4eA8J21IgQ1FHNUCQQCMjDQr69FI1w4f+Ri6mYrns6ChD+ZgHj/J+3BveDk0YCRkUpC75WNaCUj6mtecip8We4e4LCfbPoCYEzmBab65AkEAnSlxB4Gz92Co5ky4a5T/FIjp6xya7DGt+B/176J0Gz2oDePUJc0Wr3kgiYOYLYGKoYmQi1+rbrcapQWEXflsSQ==
-----END RSA PRIVATE KEY-----'''

  #公钥文件
pubKey = '''-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCe8QkU8a/AUKWu1vc5PRoKYnNnul2+B6RES0ZdBR7P+oL0tfia700OEVgPnSgRpQRiDG+aAt+H1R2mSd8FM/e2OWoB42jux+1Ex8aoyjSaZKjR55N6vTmwCZuEzn2d3aX38ncYTzWQIoUwvf2vujQ7E5ixBXu2R2YvSpzJne7bvwIDAQAB-----END PUBLIC KEY-----'''

  #alipay_pub_key
alipay_pub_key = '''MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDI6d306Q8fIfCOaTXyiUeJHkrIvYISRcc73s3vF1ZT7XN8RNPwJxo8pWaJMmvyTn9N4HQ632qJBVHf8sxHi/fEsraprwCtzvzQETrNRwVxLO5jVmRGi60j8Ue1efIlzPXV9je9mkjzOmdssymZkh2QhUrCmZYI/FCEa3/cNMW0QIDAQAB'''

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
              'charset'         :   "utf-8", 
              'sign_type'       :   "RSA",
              'version'         :   "1.0",
              'timestamp'       :   timestamp,
              #'notify_url'      :   notifyurl,
              #'return_url'      :   returnurl,   
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
        #url = "URL:"+rlt[1:]
        #print(url)
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
       
        ele=""
        ks = self.conf.keys()
        ks = sorted(ks)
       
        for k in ks:
          if self.conf[k]==None or len(self.conf[k])==0 :
            continue
          ele = ele + " <input type='hidden' name='%s' value='%s' />" % (k,self.conf[k])
          html='''
            <form name='alipaysubmit' action='%s' method='%s' target='_blank'>
                %s
                <input type="submit" value="%s" />
            </form>
            ''' % (gateway,method,ele,title)
        return html
        

    def sign_rsa(self, data):
      key = RSA.importKey(priKey)
      h = SHA.new(data.encode('utf-8'))
      signer = PKCS1_v1_5.new(key)
      signature = signer.sign(h)
      return base64.b64encode(signature).decode('utf-8')

    def sign2(self, data):
      reskey = RSA.importKey(priKey)
      signer = PKCS1_v1_5.new(reskey)
      digest = SHA256.new()
      digest.update(b64decode(data))
      sign = signer.sign(digest)
      return b64encode(sign).decode('utf-8')



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