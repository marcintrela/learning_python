"""movies URL Configuration

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
from webmovie.views import Movies, MovieDetails, PersonList, PersonAdd, PersonEdit, MovieEdit, AddMovie, DeleteMovie

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^movies/$', Movies.as_view()),
    url(r'^movie_details/(?P<id>(\d)+)/$', MovieDetails.as_view()),
    url(r'^person_list/$', PersonList.as_view()),
    url(r'^(?P<id>(\d)+)/$', PersonList.as_view()),
    url(r'^person_list/new/$', PersonAdd.as_view()),
    url(r'^person_list/(?P<id>(\d)+)/$', PersonEdit.as_view()),
    url(r'^movies/(?P<id>(\d)+)/$', MovieEdit.as_view()),
    url(r'^movies/add_movie/$', AddMovie.as_view()),
    url(r'^movies/del/(?P<id>(\d)+)/$', DeleteMovie.as_view()),


]
