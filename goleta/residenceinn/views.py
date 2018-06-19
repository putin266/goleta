from rest_framework import viewsets
from rest_framework import views
from rest_framework import response
from rest_framework import status
from rest_framework import permissions
from rest_framework import mixins
from rest_framework import authentication
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from residenceinn.serializers import *
from residenceinn.models import *
from allauth.socialaccount.providers.weixin.views import WeixinOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from residenceinn.sms_send import SmsSender
from residenceinn import smsconst
import datetime
from datetime import timezone
import json


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class AppViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = []
    queryset = App.objects.all()
    serializer_class = AppSerializer


class PaginatedAppView(views.APIView):
    """
    API endpoint that allows paginated groups to be viewed or edited.
    """
    permission_classes = []

    def get(self, request):
        applist = App.objects.order_by('id').all()
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(applist, request)
        serializer = AppSerializer(result_page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)


class AppLabelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = []
    queryset = AppLabel.objects.all()
    serializer_class = AppLabelSerializer


class ShortNewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = []
    queryset = ShortNews.objects.all()
    serializer_class = ShortNewsSerializer


class BannerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = []
    # authentication_classes = (OAuth2Authentication,)
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class IndexView(views.APIView):
    """
    API endpoint that allows index to be viewed.
    """
    permission_classes = []

    def get(self, request):
        return_data = {}
        bannerlist = BannerSerializer(Banner.objects.filter(type=1).all(), many=True)
        return_data['bannerlist'] = bannerlist.data
        applabellist = AppLabelSerializerForIndex(AppLabel.objects.filter(type=1).all(), many=True)
        return_data['applist'] = applabellist.data
        return response.Response(return_data, status.HTTP_200_OK)


class SeletedAppsView(views.APIView):
    """
    API endpoint that allows selected apps to be viewed.
    """
    permission_classes = []

    def get(self, request):
        return_data = {}
        bannerlist = BannerSerializer(Banner.objects.filter(type=2).all(), many=True)
        return_data['bannerlist'] = bannerlist.data
        applabellist = AppLabelSerializer(AppLabel.objects.filter(type=2).all()[0])
        return_data['applist'] = applabellist.data
        return response.Response(return_data, status.HTTP_200_OK)


class AppLeaderBoardView(views.APIView):
    """
    API endpoint that allows app leader board to be viewed.
    """
    permission_classes = []

    def get(self, request):
        return_data = {}
        applabellist = AppSerializer(App.objects.filter(leaderboard_index__gt=0).order_by('leaderboard_index'), many=True)
        return_data['applist'] = applabellist.data
        return response.Response(return_data, status.HTTP_200_OK)


class AppSearchView(views.APIView):
    """
    API endpoint that allows app search to be viewed.
    """
    permission_classes = []

    def get(self, request, app_name):
        return_data = {}
        applist = []
        for app in App.objects.all():
            if app_name.lower() in app.app_name.lower():
                applist.append(app)
        applabellist = AppSerializer(applist, many=True)
        return_data['applist'] = applabellist.data
        return response.Response(return_data, status.HTTP_200_OK)


class WeiXinLogin(SocialLoginView):
    adapter_class = WeixinOAuth2Adapter


class TransactionListView(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    API endpoint that allows transactions to be viewed
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        try:
            wallet = Wallet.objects.get(owner=self.request.user)
        except Wallet.DoesNotExist:
            return []
        return Transaction.objects.filter(wallet=wallet)


class SendConfirmationCodeView(views.APIView):
    """
    API endpoint that let server to send a sms code
    """
    permission_classes = []

    def get(self, request, mobile_number):
        if mobile_number == '':
            return
        try:
            keyvalue = KeyValue.objects.get(key=mobile_number)
            if keyvalue.date_created + datetime.timedelta(minutes=1) > datetime.datetime.now(timezone.utc):
                return
            else:
                keyvalue.value = self.get_new_salt()
                keyvalue.date_created = datetime.datetime.now(timezone.utc)
                keyvalue.date_expired = keyvalue.date_created + datetime.timedelta(minutes=5)
        except KeyValue.DoesNotExist:
            keyvalue = KeyValue.objects.create(key=mobile_number, value=self.get_new_salt(),
                                               date_created=datetime.datetime.now(timezone.utc),
                                               date_expired=datetime.datetime.now(timezone.utc) + datetime.timedelta(minutes=5))
        keyvalue.save()
        params = '{"code":"' + keyvalue.value + '"}'
        return_data = SmsSender.send_sms('', mobile_number, smsconst.SMS_SIGN, smsconst.SMS_TEMPLATE_CODE_REG, params).decode('utf-8')
        return response.Response(json.loads(return_data), status.HTTP_200_OK)

    @staticmethod
    def get_new_salt():
        return ''.join(random.sample(string.digits, 6))


class SendPasswordResetSmsCodeView(views.APIView):
    """
    API endpoint that let server to send a sms code
    """
    permission_classes = []

    def get(self, request, mobile_number):
        if mobile_number == '':
            return
        try:
            keyvalue = KeyValue.objects.get(key='reset' + mobile_number)
            if keyvalue.date_created + datetime.timedelta(minutes=1) > datetime.datetime.now(timezone.utc):
                return
            else:
                keyvalue.value = self.get_new_salt()
                keyvalue.date_created = datetime.datetime.now(timezone.utc)
                keyvalue.date_expired = keyvalue.date_created + datetime.timedelta(minutes=5)
        except KeyValue.DoesNotExist:
            keyvalue = KeyValue.objects.create(key='reset' + mobile_number, value=self.get_new_salt(),
                                               date_created=datetime.datetime.now(timezone.utc),
                                               date_expired=datetime.datetime.now(timezone.utc) + datetime.timedelta(minutes=5))
        keyvalue.save()
        params = '{"code":"' + keyvalue.value + '"}'
        return_data = SmsSender.send_sms('', mobile_number, smsconst.SMS_SIGN, smsconst.SMS_TEMPLATE_CODE_RESET,
                                         params).decode('utf-8')
        return response.Response(json.loads(return_data), status.HTTP_200_OK)

    @staticmethod
    def get_new_salt():
        return ''.join(random.sample(string.digits, 6))



