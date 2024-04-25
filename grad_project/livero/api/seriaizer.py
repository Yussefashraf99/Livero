from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser

from livero.models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = Users.objects.create_user(**validated_data)
            return user


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = '__all__'


class TestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tests
        fields = '__all__'


class SymptomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptoms
        fields = '__all__'


class ChronicDiseasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChronicDiseases
        fields = '__all__'


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'


class SymptomsTestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomsTests
        fields = '__all__'


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = '__all__'


class MedicineAllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = '__all__'


class ReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Readings
        fields = '__all__'


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["user_id"] = str(user.id)
        return token

    def handel_error(self, error):
        # print(error)
        if isinstance(error.detail, list) and len(error.detail) == 1:
            error.detail = error.detail[0]
        elif isinstance(error.detail, str):
            pass
            # error_response.data = get_response(
            #     message=error[0], status_code=error_response.status_code)
        elif isinstance(error, dict):
            pass
        raise error

    def validate(self, attrs):
        username = attrs.get("email")
        data = {}

        user = Users.objects.get(email=username)
        user_ser = UsersSerializer(user).data
        attrs["email"] = user.email
        if user.is_deleted:
            error = serializers.ValidationError(
                {"error": "There is no account with these credentials"}
            )
            self.handel_error(error)
        if not user.is_verified:
            error = serializers.ValidationError(
                {"error": "This User Is Not Verified"}
            )
            self.handel_error(error)

        data = super(LoginSerializer, self).validate(attrs)

        data['user_data'] = user_ser
        return data

    def to_internal_value(self, data):
        try:
            # print(data)
            return super().to_internal_value(data)
        except serializers.ValidationError as error:
            # print(error)
            if isinstance(error.detail, list) and len(error.detail) == 1:
                error.detail = error.detail[0]
            raise error


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = (
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
            "age",
            "weight",
            "gender"
        )
        extra_kwargs = {
            "first_name": {'required': True},
            "last_name": {"required": True},
            "email": {"required": True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "password fields didn't match."}
            )
        return attrs

    def create(self, validated_date):
        user = Users.objects.create(
            email=validated_date["email"],
            first_name=validated_date["first_name"],
            last_name=validated_date["last_name"],
            age=validated_date["age"],
            gender=validated_date["gender"],
            weight=validated_date["weight"]
        )
        user.set_password(validated_date["password"])
        user.save()

        return user


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospitals
        fields = "__all__"


class LapsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laps
        fields = "__all__"
