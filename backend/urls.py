from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler400,handler403,handler404,handler500

urlpatterns=[
    # 技能競賽
    path("45regional/",include("45regional.url"),name="45regional"), # 45regional
    path("46nationalmoduled/",include("46nationalmoduled.url"),name="46nationalmoduled"), # 46nationalmoduled
    path("51regional/",include("51regional.url"),name="51regional"), # 51regional
    path("52nationalmodulee/",include("52nationalmodulee.url"),name="52nationalmodulee"), # 46nationalmoduled
    path("53regional/",include("53regional.url"),name="53regional"), # 53regional
    path("worldskill2022modulec/",include("ws2022modulec.url"),name="ws2022modulec"), # worldskill2022modulec

    # 自用
    path("chclass/",include("chclass.url"),name="chclass"), # chclass
    path("chrisjudge/",include("chrisjudge.url"),name="chrisjudge"), # chclass
]

# handler400=view.error400
# handler403=view.error403
# handler404=view.error404
# handler500=view.error500