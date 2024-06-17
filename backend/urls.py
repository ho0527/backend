from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static

# from rest_framework.routers import DefaultRouter
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi


# # router=DefaultRouter()
# schema_view=get_schema_view(
#     openapi.Info(
#         title="Snippets API",
#         default_version='v1',
#         description="Test description",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="contact@snippets.local"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=[permissions.AllowAny],
# )

urlpatterns=[
    # 技能競賽
    path("45regional/",include("45regional.url"),name="45regional"), # 45regional
    path("46nationalmoduled/",include("46nationalmoduled.url"),name="46nationalmoduled"), # 46nationalmoduled
    path("50nationalmodulea/",include("50nationalmodulea.url"),name="50nationalmodulea"), # 50nationalmodulea
    path("51regional/",include("51regional.url"),name="51regional"), # 51regional
    path("51nationalmoduled/",include("51nationalmoduled.url"),name="51nationalmoduled"), # 51nationalmoduled
    path("53regional/",include("53regional.url"),name="53regional"), # 53regional
    path("53stage2modulea/",include("53stage2modulea.url"),name="53stage2modulea"), # 53stage2modulea
    path("54regional/",include("54regional.url"),name="54regional"), # 54regional
    path("worldskill2022modulec/",include("ws2022modulec.url"),name="ws2022modulec"), # worldskill2022modulec

    # 自用
    path("templ/",include("templ.url"),name="templ"), # templ
    path("chclass/",include("chclass.url"),name="chclass"), # chclass
    path("chrisjudge/",include("chrisjudge.url"),name="chrisjudge"), # chrisjudge
    path("chrisjudge_54national/",include("chrisjudge_54national.url"),name="chrisjudge_54national"), # chrisjudge_54national
    path("dcbot/",include("dcbot.url"),name="dcbot"), # dcbot
    path("tutorial/",include("tutorial.url"),name="tutorial"), # tutorial
    path("computercontroller/",include("computercontroller.url"),name="computercontroller"), # computercontroller
    path("filemanager/",include("filemanager.url"),name="filemanager"), # filemanager

    # 專案
    path("case00005/",include("case00005.url"),name="case00005"), # case00005
    path("project00009/",include("project00009.url"),name="project00009"), # project00009

    # docs
    # path('admin/',admin.site.urls),

    # # for rest_framework
    # # path('api/',include(router.urls)),
    # # for rest_framework auth
    # path('api-auth/',include('rest_framework.urls',namespace='rest_framework')),

    # re_path("swagger(?P<format>\.json|\.yaml)$",schema_view.without_ui(cache_timeout=0),name="schema-json"),
    # re_path("swagger$",schema_view.with_ui("swagger",cache_timeout=0),name="schema-swagger-ui"),
    # re_path("redoc$",schema_view.with_ui("redoc",cache_timeout=0),name="schema-redoc"),
]