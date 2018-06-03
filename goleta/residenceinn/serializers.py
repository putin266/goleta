from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework import pagination
from rest_framework.fields import SerializerMethodField

from residenceinn.models import *



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = '__all__'


class AppLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppLabel
        fields = '__all__'
        depth = 1


class AppLabelSerializerForIndex(serializers.ModelSerializer):
    apps = SerializerMethodField()

    def get_apps(self, label):
        label = AppLabel.objects.filter(id=label.id).first()
        return AppSerializer(label.apps.all()[:4], many=True).data

    class Meta:
        model = AppLabel
        fields = '__all__'
        depth = 1


class ShortNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortNews
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'
