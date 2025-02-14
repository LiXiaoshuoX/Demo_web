import json
import logging
from django.shortcuts import render, redirect
from Dash.server.init_permission import init_permission
from Dash.models import UserInfo, Role
from django.conf import settings
from django_db_logger.models import LogEntry
from django_db_logger.models import StatusLog
global ARROW

logger = logging.getLogger('db')
# Create your views here.
def index(request):
    print("Hello index")
    return render(request, "Dash/index.html")

def login(request):
    error_login = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        error_login = "帐号或密码错误"
        for User_Info in UserInfo.objects.all():
            if User_Info.name == username:
                if User_Info.password == password:
                    init_permission(request, User_Info)

                    if request.POST.get("remember_me"):
                        request.session.set_expiry(1209600)
                    else:
                        request.session.set_expiry(0)
                    return redirect("admin")
                else:
                    break

    return render(request, "Dash/login.html", {"error" : error_login})
def logup(request):
    error_logup = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        error_logup = None
        for Info in UserInfo.objects.all():
            if Info.name == username:
                error_logup = "该用户名已注册"
                break

        if not error_logup:
            user = UserInfo.objects.create(name = username, password = password)
            user.roles.set([Role.objects.get(name = "ordinary user"),]) # type: ignore
            logger.info("%s logup", username)
            return render(request, "Dash/login.html", {"error": error_logup})

    return render(request, "Dash/logup.html", {"error" : error_logup})
def logout(request):
    request.session.flush()
    logger.info("%s logout", request.session.get("operator"))
    return render(request, "Dash/login.html")

def admin(request):
    logger.info("%s login", request.session.get("operator"))
    return render(request, "Dash/admin.html")

def userinfo(request, url_code = None):
    # url_code = getattr(request, 'url_code', None)
    # url_code = request.resolver_match.kwargs
    flag = False
    error_add = []
    error_del = None
    name_list = []
    being = False
    old_password = None
    error_edit = None
    global ARROW
    flag_user = False
    match url_code:

        case "list/":
            for info in UserInfo.objects.all():
                name_list.append(info.name)
            logger.info("%s list userinfo", request.session.get("operator"))

        case "add/":
            if request.method == "POST":
                username = request.POST.getlist("username")
                password = request.POST.getlist("password")
                user_dict = dict(zip(username,password))
                print(user_dict)
                for name,word in user_dict.items():
                    print(name, word)
                    if name:
                        for info in UserInfo.objects.all():
                            if info.name == name:
                                error_add.append(name)
                                flag = True
                                break
                    else:
                        error_add.append(' ')
                        flag = True
                    if not flag:
                        print("Create user", name)
                        user = UserInfo.objects.create(name = name, password = word)
                        user.roles.set([Role.objects.get(name="ordinary user"), ]) # type: ignore
                        logger.info("%s create user %s", request.session.get("operator"), name)
                    flag = False
                flag = True
                # redirect("/admin/userinfo/add/", {"flag" : flag, "error_add" : error_add})
                # request.method = "GET"


        case "edit/":
            if request.method == "POST":
                old_name = request.POST.get("old_name")
                if old_name:
                    for Info in UserInfo.objects.all():
                        if Info.name == old_name:
                            old_password = Info.password
                            ARROW = old_name
                            being = True
                            break
                    if not being:
                        error_edit = "无此用户！"
                else:
                    new_name = request.POST.get("new_name")
                    for Info in UserInfo.objects.all():
                        if Info.name == new_name or not new_name:
                            error_edit = "用户名冲突！"
                            break
                    new_password = request.POST.get("new_password")
                    if not new_password:
                        error_edit = error_edit.join("密码为空！")
                    if not error_edit:
                        user = UserInfo.objects.get(name = ARROW)
                        user.name = new_name
                        user.password = new_password
                        user.save()
                        logger.info("%s edit user %s to %s", request.session.get("operator"), ARROW, new_name)
                        error_edit = "修改成功！"


        case "delete/":
            if request.method == "POST":
                name = request.POST.get("username")
                for Info in UserInfo.objects.all():
                    if Info.name == name:
                        for role in Info.roles.all():
                            if role.name == "administrator":
                                flag = True
                                break
                        if flag:
                            error_del = "administrator 用户无法删除！"
                        else:
                            UserInfo.delete(UserInfo.objects.get(name = name))
                            logger.info("%s delete user %s", request.session.get("operator"), name)
                            error_del = "删除成功！"
                        break
                else:
                    error_del = "无此用户！"

        case _:
            pass
    # print("error_add", error_add)
    return render(request, "Dash/userinfo.html", {"url_code" : url_code, "name_list" : name_list, "error_del" : error_del, "flag" : flag, "being" : being, "old_password" : old_password, "error_add" : error_add, "error_edit" : error_edit})

def log(request):
    # log_data = StatusLog.objects.all()
    # print("log_data", log_data)
    # for logg in log_data:
    #     print(f"{logg.create_datetime} - {logg.level}: {logg.msg}")
    logger.info("%s log", request.session.get("operator"))
    logs = StatusLog.objects.all().order_by('-create_datetime')[:100]  # 获取最新的 100 条日志

    log_data = [
        {
            'level': logging.getLevelName(logg.level),
            'message': logg.msg,
            'create_datetime': logg.create_datetime,
        }
        for logg in logs
    ]
    # print("log_data", log_data)
    return render(request, "Dash/log.html", {"log_data" : log_data})