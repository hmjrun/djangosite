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
import rsa

AliPay_Pub_Key = '''MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDI6d306Q8fIfCOaTXyiUeJHkrIvYISRcc73s3vF1ZT7XN8RNPwJxo8pWaJMmvyTn9N4HQ632qJBVHf8sxHi/fEsraprwCtzvzQETrNRwVxLO5jVmRGi60j8Ue1efIlzPXV9je9mkjzOmdssymZkh2QhUrCmZYI/FCEa3/cNMW0QIDAQAB'''

verfyURL={
    "https":"https://www.alipay.com/cooperate/gateway.do?service=notify_verify",
    "http" :"http://notify.alipay.com/trade/notify_query.do?",
    }

gateway = "https://openapi.alipay.com/gateway.do"

SIGN_TYPE = "SHA-1"

class alipay_rsa:

    def __init__(self,app_id="app_id",notifyurl="异步通知回调URL",returnurl="跳转回调URL"):
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            self.conf={
              'app_id'          :   app_id,
              'method'          :  "alipay.trade.wap.pay",
              'charset'         :   "utf-8", 
              'sign_type'       :   "RSA",
              'version'         :   "1.0",
              'timestamp'       :   timestamp,
              'notify_url'      :   notifyurl,
              'return_url'      :   returnurl,   
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

      # '''
      #   生成提交到支付宝的表单，用户通过此表单将订单信息提交到支付宝。
        
      #   由params参数提供订单信息，必须包含以下几项内容：
      #   out_trade_no：订单号
      #   subject     :订单名称、或商品名称
      #   body        :订单备注、描述
      #   total_fee   :总额
      # '''
    def createPayForm(self,params,method="POST",title="确认，支付宝付款"):

        self.conf['biz_content'] = params

        #筛选,排序,组成待签名字符串
        #wait_sign_str = self.populateURLStr(self.conf)
        wait_sign_str = '''{"a":"123"}'''
        print ("wait_sign_str: " + wait_sign_str)

        #签名RSA
        sign = self.sign(data=wait_sign_str)
        #sign = urllib.parse.quote_plus(sign)
        print (sign)
      
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
      from alipay_py import alipay_config
      private_key = rsa.PrivateKey._load_pkcs1_pem(alipay_config.RSA_PRIVATE)
      h = SHA.new(data.encode('utf-8'))
      signer = PKCS1_v1_5.new(private_key)
      signature = signer.sign(h)
      return base64.b64encode(signature)

    def make_sign(slef,data):
        """
        签名
        :param message:
        :return:
        """
        from alipay_py import alipay_config
        private_key = rsa.PrivateKey._load_pkcs1_pem(alipay_config.RSA_PRIVATE)
        sign = rsa.sign(data.encode('utf-8'), private_key, SIGN_TYPE)
        b64sing = base64.b64encode(sign)
        return b64sing

    def sign(self,data):
      from M2Crypto import EVP
      from alipay_py import alipay_config
      key = EVP.load_key_string(alipay_config.RSA_PRIVATE)
      key.reset_context(md='sha1')
      key.sign_init()
      key.sign_update(data)
      sign = base64.b64encode(key.sign_final())
      return quote(sign)
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
