from django.db import models
from django.contrib.auth.models import User, Group


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    nickname = models.CharField(max_length=200, null=True, blank=True)
    inviter = models.ForeignKey(User, related_name='inviter', null=True, on_delete=models.SET_NULL)
    mobile_number = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    invitation_code = models.CharField(max_length=254, blank=True, null=True, db_index=True)


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
    leaderboard_index = models.IntegerField(blank=True, null=True)
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


class AppDetail(models.Model):
    id = models.AutoField(primary_key=True)
    app = models.OneToOneField(App, on_delete=models.CASCADE, db_index=True)
    app_desc = models.TextField(blank=True, null=True)


class AppDetailImage(models.Model):
    id = models.AutoField(primary_key=True)
    app_detail = models.ForeignKey(AppDetail, on_delete=models.CASCADE, db_index=True)
    index = models.IntegerField(default=1, blank=True, null=True)
    image = models.ImageField(upload_to='upload/app/detail/', blank=True, null=True)


class AppLabel(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    cn_name = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to='upload/app_label/icon/', blank=True, null=True)
    web_url = models.TextField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    apps = models.ManyToManyField(App)


class Banner(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='banner/', blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
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


class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=12)


class Transaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)
    trans_type = models.CharField(max_length=254)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    trans_date = models.DateTimeField(auto_now_add=True)


class KeyValue(models.Model):
    key = models.CharField(max_length=254, primary_key=True)
    value = models.TextField(null=True, blank=True)
    date_expired = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)


class AirDrop(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=254, db_index=True)
    coin_name = models.CharField(max_length=254)
    desc = models.TextField(blank=True, null=True)
    airdrop_url = models.CharField(max_length=254, blank=True, null=True)
    starts = models.IntegerField(null=True, blank=True)
    record_date = models.DateTimeField(blank=True, null=True)
    is_need_apply = models.BooleanField(default=False)
    is_ethereum = models.BooleanField(default=False)
    is_mail = models.BooleanField(default=False)
    is_mobile = models.BooleanField(default=False)
    is_telegram = models.BooleanField(default=False)
    is_twitter = models.BooleanField(default=False)
    index = models.IntegerField(default=99)
