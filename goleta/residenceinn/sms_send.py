# -*- coding: utf-8 -*-
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
from residenceinn import smsconst


class SmsSender:

    @staticmethod
    def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
        REGION = "cn-hangzhou"
        PRODUCT_NAME = "Dysmsapi"
        DOMAIN = "dysmsapi.aliyuncs.com"
        acs_client = AcsClient(smsconst.ACCESS_KEY_ID, smsconst.ACCESS_KEY_SECRET, REGION)
        region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

        if business_id == '':
            business_id = uuid.uuid1()
        smsRequest = SendSmsRequest.SendSmsRequest()
        smsRequest.set_TemplateCode(template_code)
        if template_param is not None:
            smsRequest.set_TemplateParam(template_param)
        smsRequest.set_OutId(business_id)
        smsRequest.set_SignName(sign_name)
        smsRequest.set_PhoneNumbers(phone_numbers)
        smsResponse = acs_client.do_action_with_exception(smsRequest)

        return smsResponse




