from kavenegar import *
from random import randint
import time
import datetime

from config.settings import kavenegar_API
from .models import AgentCustomUserModel


def send_otp(phone_number, otp):
    time.sleep(2)
    phone_number = [phone_number, ]
    try:
        api = KavenegarAPI(kavenegar_API)
        params = {
            'receptor': phone_number,
            'template': 'PhoneLoginTest',
            'token': f'{otp}',
            # 'token2': 'لاگین آزمایشی هومبیا',
            # 'token3': '',
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def get_random_otp():
    return randint(10000, 99999)


def otp_time_checker(phone_number):
    try:
        user = AgentCustomUserModel.objects.get(phone_number=phone_number)
        now_time = datetime.datetime.now()
        otp_time = user.otp_code_datetime_created
        diff_time = now_time - otp_time
        print('DIFF TIME: ', diff_time)
        if diff_time.seconds > 30:  # better: 120
            return False
        return True
    except AgentCustomUserModel.DoesNotExist:
        return False


def phone_checker(phone):
    try:
        if len(phone) == 11 and int(phone) and phone[0:2] == '09' and phone[2] in ['0', '1', '2', '3']:
            return True
    except ValueError:
        return False


def otp_checker(otp):
    try:
        if len(otp) == 5 and int(otp):
            return True
    except ValueError:
        return False

