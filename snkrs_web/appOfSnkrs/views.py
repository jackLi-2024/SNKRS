from django.shortcuts import render, HttpResponse, redirect
from appOfSnkrs import models
import json
# Create your views here.

# 账号列表


def account_list(request):
    ret = models.Account.objects.all().order_by("id")
    # if request.is_ajax():
    if request.method == "POST":
        phone = request.POST.get("phone",None)
        password = request.POST.get("password",None)
        print(phone)
        print(password)
        # if len(phone) != 11:
        #     error = {"msg": "手机号码错误"}
        #     print("错误手机号")
        # return HttpResponse(json.dumps(error))
    return render(request, "account_list.html", {"account_list": ret})

# # 添加账号
# def add_account(request):
#     if request.is_ajax():
#         phone = request.POST.get("phone")
#         password = request.POST.get("password")
#         print(phone)
#         print(password)


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
