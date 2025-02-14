from django.conf import settings
from django.shortcuts import HttpResponse, redirect
from django.utils.deprecation import MiddlewareMixin
import logging
import re

from Dash.views import logger

class RBACMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        #Before
        flag = False
        # print(request)
        # if request.resolver_match:
        #     url_params = request.resolver_match.kwargs
        #     for key, value in url_params.items():
        #         setattr(request, key, value)
        # request.url_code = request.resolver_match.kwargs.get('url_code')
        # print(request.url_code)

        request_url = request.path_info
        print("RBAC server!", request_url)

        for url in settings.SAFE_URLS:
            if re.match(url, request_url):
                flag = True
                print("safe url!")
                break

        if not flag:
            if request.session.get(settings.PERMISSION_URL_KEY, False):
                permission_url = request.session.get(settings.PERMISSION_URL_KEY)
                print("RBAC permission url:", permission_url)
                # if request.user.is_superuser:
                #     return None

                # if not permission_url:
                #     redirect("login/")

                for perm_group_id, code_url in permission_url.items():
                    if int(perm_group_id) == 1:
                        print("Power!")
                        break

                    for url in code_url['urls']:
                        urlpattern = "^/{0}$".format(url)
                        print("urlpattern", urlpattern)
                        if re.match(urlpattern, request_url):
                            request.session['permission_code'] = code_url['codes']
                            flag = True
                            break

                    if not flag:
                        if settings.DEBUG:
                            info = '<br>' + ('<br>'.join(code_url['urls']))
                            return HttpResponse("No permission code found!<br><tab>" + info)
                        else:
                            return HttpResponse("No permission code found!")
                        logger.warning("%s No permission code for %s",request.session.get("operator"), request_url)
                    else:
                        break
            else:
                print("redirect login")
                return redirect("login")
        print("OK!")

        # request.body_data = request.read()
        response = self.get_response(request)
        #After

        return response

    def process_request(self, request):
        pass
