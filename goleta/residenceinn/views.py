from rest_framework import viewsets
from rest_framework import pagination
from rest_framework import views
from rest_framework import response
from rest_framework import status
from residenceinn.serializers import *
from residenceinn.models import *
import json


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
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
        applist = App.objects.all()
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(applist, request)
        serializer = AppSerializer(result_page, many=True)
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
        bannerlist = BannerSerializer(Banner.objects.all(), many=True)
        return_data['bannerlist'] = bannerlist.data
        applabellist = AppLabelSerializerForIndex(AppLabel.objects.all(), many=True)
        return_data['applist'] = applabellist.data
        return response.Response(return_data, status.HTTP_200_OK)



