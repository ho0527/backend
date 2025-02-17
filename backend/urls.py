from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static

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
    path("55regional/",include("55regional.url"),name="55regional"), # 55regional
    path("worldskill2022modulec/",include("ws2022modulec.url"),name="ws2022modulec"), # worldskill2022modulec
    path("worldskill2024moduleb/",include("worldskill2024moduleb.url"),name="worldskill2024moduleb"), # worldskill2022modulec

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
]