# 在celery_tasks目录下创建config.py文件，用于保存celery的配置信息

broker_url = "redis://127.0.0.1/14"
# 在celery_tasks目录下创建main.py文件，用于作为celery的启动文件

from celery import Celery

# 为celery使用django配置文件进行设置
import os

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'my_django.settings.dev'

# 创建celery应用
app = Celery('django_celery')

# 导入celery配置
app.config_from_object('celery_tasks.config')

# 自动注册celery任务
app.autodiscover_tasks(['celery_tasks.sms'])


# 在celery_tasks目录下创建sms目录，用于放置发送短信的异步任务相关代码。
# 将提供的发送短信的云通讯SDK放到celery_tasks/sms/目录下。
# 在celery_tasks/sms/目录下创建tasks.py文件，用于保存发送短信的异步任务

import logging

from celery_tasks.main import app
from .yuntongxun.sms import CCP

logger = logging.getLogger("django")

# 验证码短信模板
SMS_CODE_TEMP_ID = 1


# 调用第三方的api

@app.task(name='send_sms_code')
def send_sms_code(mobile, code, expires):
    """
    发送短信验证码
    :param mobile: 手机号
    :param code: 验证码
    :param expires: 有效期
    :return: None
    """

    try:
        ccp = CCP()
        result = ccp.send_template_sms(mobile, [code, expires], SMS_CODE_TEMP_ID)
    except Exception as e:
        logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
    else:
        if result == 0:
            logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)
        else:
            logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)


# 在views.py中改写SMSCodeView视图，使用celery异步任务发送短信

from celery_tasks.sms import tasks as sms_tasks


class SMSCodeView(GenericAPIView):
    ...
    # 发送短信验证码
    sms_code_expires = str(300 // 60)
    sms_tasks.send_sms_code.delay(mobile, sms_code, 300)

    return Response({"message": "OK"})

