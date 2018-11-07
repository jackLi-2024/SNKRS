import sys
import os.path as path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from django.shortcuts import render, HttpResponse, redirect
from appOfSnkrs import models
from snkrs_backserver.login.login import *
import json



# Create your views here.

# 账号列表
def account_list(request):
    ret = models.Account.objects.all().order_by("id")
    return render(request, "account_list.html", {"account_list": ret})

# 添加账号
def add_account(request):
    if request.is_ajax():
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        print(phone)
        print(password)
        loginer = Loginer(username=phone, password=password, headless=True)
        print(loginer.username)
        if loginer.login(url="https://www.nike.com/cn/launch/").get("status", "-1") != "1":
            error = {"msg": "手机号码错误"}
            loginer.B.close()
            return HttpResponse(json.dumps(error))
        else:
            ret = models.Account.objects.all().order_by("id")
            return render(request, "account_list.html", {"account_list": ret})


# # 添加账号
# def add_account(request):
#     error_msg = ""
#     if request.method == "POST":
#         phone = request.POST.get("phone", None)
#         password = request.POST.get("password", None)
#         print(phone)
#         print(password)
#         # if new_name:
#         #     models.Account.objects.create(name=new_name)
#         #     return redirect("/account_list/")
#         # else:
#         #     error_msg = "出版社名字不能为空!"
#     return render(request, "account_list.html", {"error": error_msg})
