from django.shortcuts import render
from first.models import Videomodel
from users.models import MyUser
from django.http import Http404
from rest_framework import status
from first.serializers import videoSerializer 
from rest_framework.response import  Response
from first.views import *
from rest_framework.permissions import IsAuthenticated
import os 
from users.serializers import RegistrationSerializer,UpdateUserProfile
from rest_framework.authentication import TokenAuthentication,BasicAuthentication,SessionAuthentication
from rest_framework.views import APIView

from rest_framework.pagination import PageNumberPagination
# Create your views here.

def check_user(self,request):
        if request.user.role==True:
            return True
        return False

class AllUsers(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,BasicAuthentication,SessionAuthentication)
    pagination_class=MyPagination() 

    def get(self, request, format=None):
        role=check_user(self,request)
        if role==True:
            queryset = MyUser.objects.all()
            paginated_queryset = self.pagination_class.paginate_queryset(queryset, request)
            serializer = RegistrationSerializer(paginated_queryset, many=True)
            return self.pagination_class.get_paginated_response(serializer.data)
        return Response({'msg':'you dont have permmision '},status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request, format=None):
        role=check_user(self,request)
        if role==True:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'you dont have permmision '},status=status.HTTP_401_UNAUTHORIZED)
    
class AllUsersDetails(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,BasicAuthentication,SessionAuthentication)

    def check_user(self,request):
        if request.user.role==True:
            return True
        return False
    
    def get_object(self, pk):
        try:
            return MyUser.objects.get(pk=pk)
        except MyUser.DoesNotExist:
            raise Http404
        
    def get(self, request,pk):
        role=check_user(self,request)
        if role==True:
            transformer = self.get_object(pk)
            serializer = RegistrationSerializer(transformer)
            return Response(serializer.data)
        return Response({'msg':'you dont have permmision to see user '},status=status.HTTP_401_UNAUTHORIZED)
    
    def put(self,request,pk):
        transformer = self.get_object(pk)
        old_profile=transformer.profile.path
        serializer = UpdateUserProfile(transformer, data=request.data)
        role=check_user(self,request)
        if role==True:
            if serializer.is_valid():
                ser=serializer.save()
                new_profile=self.get_object(ser.id).profile.path
                if old_profile != new_profile:
                    if os.path.exists(old_profile):
                        os.remove(old_profile)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'you dont have permmision to update user'},status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self,request,pk):
        role=check_user(self,request)
        if role==True:
            transformer = self.get_object(pk)
            if os.path.exists(transformer.profile.path):
                os.remove(transformer.profile.path)
            obj=Videomodel.objects.filter(user=transformer)
            for i in obj:
                if os.path.exists(i.video.path):
                    os.remove(i.video.path)
                if os.path.exists(i.logo.path):
                    os.remove(i.logo.path)
                i.delete()
            transformer.delete()
            return Response({'msg':'User has been deleted'},status=status.HTTP_204_NO_CONTENT)
        return Response({'msg':'you dont have permmision to remove any user '},status=status.HTTP_401_UNAUTHORIZED)


class VideoList(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,BasicAuthentication,SessionAuthentication)
    """
    List all Transformers, or create a new Transformer
    """
    pagination_class = MyPagination()
    def get(self, request, format=None):
        role=check_user(self,request)
        if role==True:
            queryset = Videomodel.objects.all()
            paginated_queryset = self.pagination_class.paginate_queryset(queryset, request)
            serializer = videoSerializer(paginated_queryset, many=True)
            return self.pagination_class.get_paginated_response(serializer.data)
        return Response({'msg':'you dont have permmision '},status=status.HTTP_401_UNAUTHORIZED)
  
  
class VideoDetail(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,BasicAuthentication,SessionAuthentication)
    """
    Retrieve, update or delete a transformer instance
    """
    def get_object(self, pk):
        try:
            return Videomodel.objects.get(pk=pk)
        except Videomodel.DoesNotExist:
            raise Http404
  
    def get(self, request, pk, format=None):
        role=check_user(self,request)
        if role==True:
            transformer = self.get_object(pk)
            serializer = videoSerializer(transformer)
            return Response(serializer.data)
        return Response({'msg':'you dont have permmision '},status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk, format=None):
        role=check_user(self,request)
        if role==True:
            transformer = self.get_object(pk)
            removeable_video=Videomodel.objects.get(id=transformer.id).video.path
            removeable_image=Videomodel.objects.get(id=transformer.id).logo.path
            # delete fun
            if os.path.exists(removeable_video):
                os.remove(removeable_video)
            if os.path.exists(removeable_image):
                os.remove(removeable_image)
            transformer.delete()

            return Response({"msg":"deleted successfully"},status=status.HTTP_204_NO_CONTENT)
        return Response({'msg':'you dont have permmision '},status=status.HTTP_401_UNAUTHORIZED)