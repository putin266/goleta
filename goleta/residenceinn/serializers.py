import random
import string
import re
from django.utils.translation import gettext as _
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework import pagination
from rest_framework.fields import SerializerMethodField
from rest_auth.registration.serializers import RegisterSerializer
from datetime import datetime
from datetime import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.contrib.auth.models import User, Group

from residenceinn.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    inviter = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
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
        exclude = ('type',)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('trans_type', 'amount', 'trans_date')


class SendConfirmationCodeSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=20)


class ExtendedRegisterSerializer(RegisterSerializer):
    invitation_code = serializers.CharField(required=False, allow_blank=True)
    mobile_number = serializers.CharField()
    sms_code = serializers.CharField()
    email = serializers.EmailField(allow_blank=True, required=False)
    nickname = serializers.CharField(required=False, allow_blank=True)

    def validate_mobile_number(self, mobile_number):
        if not re.match(r'1\d{10}$', mobile_number):
            raise serializers.ValidationError(
                _('Invalid Mobile Number.')
            )
        if self.is_mobile_number_used(mobile_number):
            raise serializers.ValidationError(
                _('Mobile number is being used.')
            )
        return mobile_number

    def validate(self, data):
        try:
            keyvalue = KeyValue.objects.get(key=data['mobile_number'])
            if keyvalue.date_expired < datetime.now(timezone.utc) or keyvalue.value != data['sms_code']:
                raise serializers.ValidationError(
                    _('SMS password not correct.')
                )
        except KeyValue.DoesNotExist:
            raise serializers.ValidationError(
                _('SMS password not correct.')
            )
        keyvalue.delete()
        return data

    def save(self, request):
        user = super().save(request)
        user_profile_list = UserProfile.objects.filter(user=user)
        if len(user_profile_list) > 0:
            user_profile = user_profile_list[0]
        else:
            user_profile = UserProfile()
        user_profile.user = user
        user_profile.nickname = self.validated_data['nickname']
        user_profile.mobile_number = self.validated_data['mobile_number']
        user_profile.invitation_code = self.get_next_salt()
        user_profile.inviter = self.get_user_by_invitation_code(self.validated_data['invitation_code'])
        user_profile.save()

        if user_profile.inviter is not None:
            self.top_up_wallet(user_profile.inviter, 20)
            inviter_parent = user_profile.inviter.userprofile.inviter
            if inviter_parent is not None:
                self.top_up_wallet(inviter_parent, 10)

        return user

    def top_up_wallet(self, owner, amount):
        wlist = Wallet.objects.filter(owner=owner)
        if len(wlist) > 0:
            wallet = wlist[0]
        else:
            wallet = Wallet()
            wallet.owner = owner
        wallet.balance = wallet.balance + amount
        wallet.save()
        transaction = Transaction()
        transaction.amount = amount
        transaction.wallet = wallet
        transaction.trans_type = 'USER_REG'
        transaction.save()

    @staticmethod
    def get_next_salt():
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        while len(UserProfile.objects.filter(invitation_code=salt)) > 0:
            salt = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        return salt

    @staticmethod
    def get_user_by_invitation_code(code):
        uplist = UserProfile.objects.filter(invitation_code=code)
        if len(uplist) > 0:
            return uplist[0].user
        else:
            return None

    @staticmethod
    def is_mobile_number_used(mobile_number):
        return len(UserProfile.objects.filter(mobile_number=mobile_number)) > 0


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    mobile_number = serializers.CharField(max_length=20)
    sms_code = serializers.CharField(max_length=10)

    def validate(self, data):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            self.user = UserProfile.objects.get(mobile_number=data['mobile_number']).user
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError(
                _('Invalid Mobile Number.')
            )

        # Construct SetPasswordForm instance
        if not self.is_password_valid(data['new_password1'], data['new_password2']):
            raise serializers.ValidationError(
                _('Invalid password.')
            )
        if not self.is_smscode_valid(data['mobile_number'], data['sms_code']):
            raise serializers.ValidationError(
                _('SMS password not correct.')
            )

        return data

    def is_password_valid(self, password1, password2):
        if password1 == '':
            return False
        if password1 != password2:
            return False
        return True

    def is_smscode_valid(self, mobile_number, sms_code):
        try:
            keyvalue = KeyValue.objects.get(key='reset' + mobile_number)
            if keyvalue.date_expired < datetime.now(timezone.utc) or keyvalue.value != sms_code:
                return False
        except KeyValue.DoesNotExist:
            return False
        keyvalue.delete()
        return True

    def save(self):
        self.user.set_password(self.data['new_password1'])
        self.user.save()
        return self.user
