from django.db import models


class App(models.Model):
    id = models.AutoField(primary_key=True)
    app_name = models.TextField(blank=True, null=True)
    app_logo = models.ImageField(upload_to='upload/app/logo/', blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    number_downloads = models.IntegerField(blank=True, null=True)
    star = models.DecimalField(decimal_places=1, max_digits=2, null=True)
    ms = models.TextField(blank=True, null=True)
    contents = models.TextField(blank=True, null=True)
    tj_ms = models.TextField(blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    is_tj = models.BooleanField(blank=True, default=False)
    is_ph = models.BooleanField(blank=True, default=False)
    is_hot = models.BooleanField(blank=True, default=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    android_package_name = models.TextField(blank=True, null=True)
    android_apk = models.FileField(upload_to='upload/app/apk/', blank=True, null=True)
    android_version = models.CharField(max_length=254, blank=True, null=True)
    android_size = models.CharField(max_length=254, blank=True, null=True)
    android_url = models.TextField(blank=True, null=True)
    ios_url = models.TextField(blank=True, null=True)
    web_url = models.TextField(blank=True, null=True)


class AppLabel(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    cn_name = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to='upload/app_label/icon/', blank=True, null=True)
    web_url = models.TextField(blank=True, null=True)
    apps = models.ManyToManyField(App)


class Banner(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='banner/', blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)


class ShortNews(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to='upload/short_news/pic/', blank=True, null=True)
    ms = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_fav = models.BooleanField(blank=True, default=False)

