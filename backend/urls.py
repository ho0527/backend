from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler400,handler403,handler404,handler500

urlpatterns=[
    # 技能競賽
    path("46nationalmoduled/",include("46nationalmoduled.url"),name="46nationalmoduled"), # 46nationalmoduled
    path("52nationalmodulee/",include("52nationalmodulee.url"),name="52nationalmodulee"), # 46nationalmoduled
    path("53regional/",include("53regional.url"),name="53regional"), # 53regional
    path("worldskill2022modulec/",include("ws2022modulec.url"),name="ws2022modulec"), # 53regional

    # 自用
    path("chclass/",include("chclass.url"),name="chclass"), # chclass
    path("chrisjudge/",include("chrisjudge.url"),name="chrisjudge"), # chclass
]

# handler400=view.error400
# handler403=view.error403
# handler404=view.error404
# handler500=view.error500