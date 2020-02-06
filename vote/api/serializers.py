from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from vote.models import PertanyaanModel, PilihanModel


#Serializer_authentication
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')

        
class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user
        raise serializers.ValidationError('Cek Username dan Password')

#Seriliazer Vote_APP
class PilihanSerializer(serializers.ModelSerializer):

    class Meta:
        model = PilihanModel
        fields = ('id_pilihan','pilihan')

class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = PilihanModel
        fields = ('id_pilihan','pilihan','vote')
        read_only_fields = ('id_pilihan','pilihan')

class PertanyaanSerializer(serializers.ModelSerializer):

    class Meta:
        model = PertanyaanModel
        fields = ('id_pertanyaan','pertanyaan')

class PertanyaanDetailSerializer(serializers.ModelSerializer):
    kumpulan_pilihan = PilihanSerializer(many = True, read_only= True)

    class Meta:
        model = PertanyaanModel
        fields = ('id_pertanyaan','pertanyaan','kumpulan_pilihan')
        
class VotingSerializer(serializers.ModelSerializer):
    kumpulan_pilihan = VoteSerializer(many = True, read_only= True)

    class Meta:
        model = PertanyaanModel
        fields = ('id_pertanyaan','pertanyaan','kumpulan_pilihan')