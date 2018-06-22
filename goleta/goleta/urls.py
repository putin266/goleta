"""goleta URL Configuration

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
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from residenceinn import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='DAppDapp API')

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'apps', views.AppViewSet)
router.register(r'app_labels', views.AppLabelViewSet)
router.register(r'short_news', views.ShortNewsViewSet)
router.register(r'banners', views.BannerViewSet)
router.register(r'airdrop', views.AirDropViewSet)
router.register(r'mining_apps', views.MiningAppsView)
router.register(r'user_profile', views.UserProfileViewSet, base_name='user_profile')
router.register(r'transactions', views.TransactionListView, base_name='transactions')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^$', schema_view),
    url(r'^', include(router.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    #url(r'^accounts/', include('allauth.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/weixin/$', views.WeiXinLogin.as_view(), name='weixin_login'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    # url(r'^applist/', views.PaginatedAppView.as_view(), name='applist'),
    url(r'^index/', views.IndexView.as_view(), name='index'),
    url(r'^app_leader_board/', views.AppLeaderBoardView.as_view(), name='app_leader_board'),
    url(r'^selected_apps/', views.SeletedAppsView.as_view(), name='selected_apps'),
    url(r'^app_search/(?P<app_name>\w{1,50})/$', views.AppSearchView.as_view(), name='app_search'),
    url(r'^send_register_code/(?P<mobile_number>1\d{10})/$', views.SendConfirmationCodeView.as_view(),
        name='send_register_code'),
    url(r'^send_reset_code/(?P<mobile_number>1\d{10})/$', views.SendPasswordResetSmsCodeView.as_view(),
        name='send_reset_code'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
