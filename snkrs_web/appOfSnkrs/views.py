import sys
import os.path as path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from appOfSnkrs import models
from snkrs_backserver.login.login import *
import json


# Create your views here.

def account_list(request):
    if request.is_ajax():
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        loginer = Loginer(username=phone, password=password, headless=True, proxies=None, timeout=60)
        data = loginer.login(url="https://www.nike.com/cn/launch/")
        if data.get("status", "-1") != "1":
            msg = data.get("msg", "-1")
            if msg.startswith("Timeout"):
                error = {"msg": "链接超时，请稍后再试"}
            else:
                error = {"msg": "手机号码或密码错误错误"}
            return HttpResponse(json.dumps(error))
        else:
            print("登录成功")
            models.Account.objects.create(phone=phone, password=password)
            loginer.B.close()
            error = {"msg": "success"}
            return HttpResponse(json.dumps(error))
    else:
        ret = models.Account.objects.all().order_by("id")
        return render(request, "account_list.html", {"account_list": ret})
