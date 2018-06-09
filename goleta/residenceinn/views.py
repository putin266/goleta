from rest_framework import viewsets
from rest_framework import views
from rest_framework import response
from rest_framework import status
from rest_framework import permissions
from residenceinn.serializers import *
from residenceinn.models import *
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class AppViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = App.objects.all()
    serializer_class = AppSerializer


class PaginatedAppView(views.APIView):
    """
    API endpoint that allows paginated groups to be viewed or edited.
    """
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
    queryset = AppLabel.objects.all()
    serializer_class = AppLabelSerializer


class ShortNewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ShortNews.objects.all()
    serializer_class = ShortNewsSerializer


class BannerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class IndexView(views.APIView):
    """
    API endpoint that allows index to be viewed.
    """
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
    def get(self, request):
        return_data = {}
        applabellist = AppSerializer(App.objects.filter(leaderboard_index__gt=0).order_by('leaderboard_index'), many=True)
        return_data['applist'] = applabellist.data
        return response.Response(return_data, status.HTTP_200_OK)


class AppSearchView(views.APIView):
    """
    API endpoint that allows app search to be viewed.
    """
    def get(self, request, app_name):
        return_data = {}
        applist = []
        for app in App.objects.all():
            if app_name.lower() in app.app_name.lower():
                applist.append(app)
        applabellist = AppSerializer(applist, many=True)
        return_data['applist'] = applabellist.data
        return response.Response(return_data, status.HTTP_200_OK)
