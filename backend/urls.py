from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    # 技能競賽
    path("45regional/",include("45regional.url"),name="45regional"), # 45regional
    path("46nationalmoduled/",include("46nationalmoduled.url"),name="46nationalmoduled"), # 46nationalmoduled
    path("51nationalmoduled/",include("51nationalmoduled.url"),name="51nationalmoduled"), # 51nationalmoduled
    path("51regional/",include("51regional.url"),name="51regional"), # 51regional
    path("53regional/",include("53regional.url"),name="53regional"), # 53regional
    path("53stage2modulea/",include("53stage2modulea.url"),name="53stage2modulea"), # 53stage2modulea
    path("worldskill2022modulec/",include("ws2022modulec.url"),name="ws2022modulec"), # worldskill2022modulec

    # 自用
    path("chclass/",include("chclass.url"),name="chclass"), # chclass
    path("chrisjudge/",include("chrisjudge.url"),name="chrisjudge"), # chrisjudge

    # 專案
    path("project005/",include("project005.url"),name="project005"), # project005
]