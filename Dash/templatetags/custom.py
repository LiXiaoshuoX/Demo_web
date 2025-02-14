from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
import re, os

from django.utils.translation.trans_null import activate

register = template.Library()

def get_structure_data(request):
    current_url = request.path_info
    perm_menu = request.session[settings.PERM_MENU_SESSION_KEY]
    print("perm_menu", perm_menu)
    menu_dict = {}

    for item in perm_menu:
        if not item["pid_id"]:
            menu_dict[item["id"]] = item.copy()

    print("menu_dict", menu_dict)

    for item in perm_menu:
        regex = "^{0}$".format(item["url"])
        if re.match(regex, current_url):
            if not item["pid_id"]:
                menu_dict[item["id"]]["active"] = True
            else:
                menu_dict[item["pid_is"]]["active"] = True

    print("menu_dict", menu_dict)
    menu_result = {}

    for item in menu_dict.values():
        active = item.get("active")
        menu_id = item.get("menu_id")

        if menu_id in menu_result:
            menu_result[menu_id]["children"].append({"name": item["name"], "url": item["url"], "active": active})
            if active:
                menu_result[menu_id]["active"] = True
        else:
            menu_result[menu_id] = {"menu_id": item["menu_id"],"menu_name": item["menu_name"], "url": item["url"], "active": active, "children": [{"name": item["name"], "url": item["url"], "active": active}]}

        print("menu_result", menu_result)

        return menu_result

# @register.inclusion_tag(settings.TEMPLATES["DIRS"] / "Templates/rbac_menu.html")
# def rbac_menu(request):
#     menu_data = get_structure_data(request)
#     print("menu_data", menu_data)
#     return {'menu_data': menu_data}