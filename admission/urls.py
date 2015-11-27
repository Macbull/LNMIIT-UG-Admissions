"""admission URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views
from ug.viewsets import ApplicationViewSet,AdmissionDetailViewSet,ApplicantViewSet,BranchViewSet,PreferenceViewSet,RoundViewSet,AllotedSeatViewSet,WaitingListViewSet
router = SimpleRouter(trailing_slash=True)
router.register(r'api/applicant',ApplicantViewSet)
router.register(r'api/branch',BranchViewSet)
router.register(r'api/preference',PreferenceViewSet)
router.register(r'api/round',RoundViewSet)
router.register(r'api/allotedSeat',AllotedSeatViewSet)
router.register(r'api/waitingList',WaitingListViewSet)
router.register(r'api/session',AdmissionDetailViewSet)
router.register(r'api/application',ApplicationViewSet)
router.register(r'api/preference',PreferenceViewSet)


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(router.urls)),
    url(r'^obtain_auth_token/', views.obtain_auth_token)
]
