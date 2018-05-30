from django.db import models


class App(models.Model):
    id = models.AutoField(primary_key=True)
    app_name = models.TextField()
    app_logo = models.ImageField(upload_to='app/logo/')
    price = models.IntegerField()
    number_downloads = models.IntegerField()
    star = models.DecimalField(decimal_places=1, max_digits=2)
    ms = models.TextField()
    contents = models.TextField()
    tj_ms = models.TextField()
    index = models.IntegerField()
    is_tj = models.BooleanField()
    is_ph = models.BooleanField()
    is_hot = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    android_package_name = models.TextField()
    android_apk = models.FileField(upload_to='app/apk/')
    android_version = models.CharField(max_length=254)
    android_size = models.CharField(max_length=254)
    android_url = models.TextField()
    ios_url = models.TextField()


class AppLabel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    apps = models.ManyToManyField(App)


class Banner(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='banner/')
    index = models.IntegerField()


class ShortNews(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    img = models.ImageField(upload_to='short_news/pic/')
    ms = models.TextField()
    content = models.TextField()
    index = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_fav = models.BooleanField()

