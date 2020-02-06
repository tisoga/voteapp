from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from knox.auth import AuthToken

from vote.models import PertanyaanModel, PilihanModel
from vote.api.serializers import (PertanyaanSerializer, PilihanSerializer,
                                  PertanyaanDetailSerializer, VotingSerializer, VoteSerializer,
                                  RegisterSerializer, UserSerializer, LoginSerializer)

# Authentication
@api_view(['POST'])
def RegisterAPI(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'User': UserSerializer(user, context=serializer).data,
                'token': AuthToken.objects.create(user)[1]
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def LoginAPI(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({
                'User': UserSerializer(user, context=serializer).data,
                'token': AuthToken.objects.create(user)[1]
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def UserAPI(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# API
@api_view(['GET', 'POST', "DELETE"])
# @permission_classes([IsAuthenticated])
def ListVoteAPI(request):
    if request.method == 'GET':
        pertanyaan = PertanyaanModel.objects.all()
        serializer = PertanyaanSerializer(pertanyaan, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PertanyaanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        serializer = PertanyaanSerializer()


@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
# @permission_classes([IsAuthenticated])
def DetailVoteAPI(request, id_pertanyaan):
    pertanyaan = get_object_or_404(PertanyaanModel, pk=id_pertanyaan)
    if request.method == 'GET':
        serializer = PertanyaanDetailSerializer(pertanyaan)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PilihanSerializer(data=request.data)
        if serializer.is_valid():
            pilihan = serializer.save(pertanyaan=pertanyaan)
            return Response(PilihanSerializer(pilihan).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            id_pilihan = request.data['id_pilihan']
            pilihan = get_object_or_404(PilihanModel, pk=id_pilihan)
            pilihan.delete()
            return Response({'detail': 'Deleted'})
        except KeyError:
            raise NotFound()
    elif request.method == 'PATCH':
        try:
            id_pilihan = request.data['id_pilihan']
            pilihan = get_object_or_404(PilihanModel, pk=id_pilihan)
            serializer = PilihanSerializer(pilihan, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            raise NotFound()


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def VotingAPI(request, id_pertanyaan):
    pertanyaan = get_object_or_404(PertanyaanModel, pk=id_pertanyaan)
    if request.method == 'GET':
        serializer = VotingSerializer(pertanyaan)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VoteSerializer(pertanyaan, data=request.data)
        pilihan = get_object_or_404(
            PilihanModel, pk=request.data['id_pilihan'])
        if serializer.is_valid():
            serializer = VotingSerializer(pertanyaan)
            pilihan.vote += 1
            pilihan.save()
            return Response({
                "pertanyaan": serializer.data,
                "status": "Vote Sukses"
            })
        return Response(serializer.errors)
