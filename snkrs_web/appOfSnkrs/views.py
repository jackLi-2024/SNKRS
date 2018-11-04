from django.shortcuts import render, HttpResponse, redirect
from appOfSnkrs import models

# Create your views here.

# 账号列表
def account_list(request):
    ret = models.Account.objects.all().order_by("id")
    return render(request, "account_list.html", {"account_list": ret})


# 添加账号
def add_account(request):
    error_msg = ""
    if request.method == "POST":
        new_name = request.POST.get("account_name", None)
        if new_name:
            models.Account.objects.create(name=new_name)
            return redirect("/account_list/")
        else:
            error_msg = "出版社名字不能为空!"
    return render(request, "add_account.html", {"error": error_msg})