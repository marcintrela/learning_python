"""conference_room URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from reservation_room.views import AllRooms, AddRoom, DeleteRoom, ModifyRoom, ShowRoom, ReservationRoom, Search

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', AllRooms.as_view(), name='allRooms'),
    url(r'^room/(?P<id>(\d)+)/$', ShowRoom.as_view()),
    url(r'^room/new/$', AddRoom.as_view()),
    url(r'^room/delete/(?P<id>(\d)+)/$', DeleteRoom.as_view()),
    url(r'^modify/(?P<id>(\d)+)/$', ModifyRoom.as_view()),
    url(r'^reservation/(?P<id>(\d)+)/$', ReservationRoom.as_view()),
    url(r'^search/$', Search.as_view()),

]
