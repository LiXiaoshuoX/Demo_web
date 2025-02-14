from django.conf import settings

def init_permission(request, userinfo):
    print(userinfo)
    permission_item_list = userinfo.roles.values("permissions__id", "permissions__name", "permissions__url", "permissions__perm_code", "permissions__pid__id", "permissions__perm_group__id", "permissions__perm_group__menu__id", "permissions__perm_group__menu__name").distinct()
    print("permission_item_list:", permission_item_list)

    permission_url_dict = {}
    permission_menu_list = []

    for item in permission_item_list:
        perm_group_id = item["permissions__perm_group__id"]
        url = item["permissions__url"]
        perm_code = item["permissions__perm_code"]
        if perm_group_id in permission_url_dict:
            permission_url_dict[perm_group_id]["codes"].append(perm_code)
            permission_url_dict[perm_group_id]["urls"].append(url)
        else:
            permission_url_dict[perm_group_id] = {"codes": [perm_code,], "urls": [url,]}

    print("permission_url_dict:", permission_url_dict)
    request.session[settings.PERMISSION_URL_KEY] = permission_url_dict


    for item in permission_item_list:
        tpl = {"id": item["permissions__id"], "name": item["permissions__name"], "url": item["permissions__url"], "pid_id": item["permissions__pid__id"], "menu_id": item["permissions__perm_group__menu__id"], "menu_name": item["permissions__perm_group__menu__name"]}
        permission_menu_list.append(tpl)

    print("permission_menu_list", permission_menu_list)
    request.session[settings.PERMISSION_MENU_KEY] = permission_menu_list
    request.session["operator"] = userinfo.name
    request.session.save()