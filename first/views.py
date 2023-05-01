import cv2
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import videoSerializer  
from first.movie import test_video
# from .status_url import stock_url
import os
from rest_framework.authentication import TokenAuthentication,BasicAuthentication,SessionAuthentication
from .models import Videomodel
from users.models import MyUser
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.http import JsonResponse
# Create your views here.
from rest_framework.pagination import PageNumberPagination

class MyPagination(PageNumberPagination):
    page_size = 10



def get_video_resolution(video_path):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return (width, height)
class Index(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,BasicAuthentication,SessionAuthentication)
    
    pagination_class = MyPagination()
    def get(self, request, format=None):
        queryset=Videomodel.objects.filter(user=request.user)
        paginated_queryset = self.pagination_class.paginate_queryset(queryset, request)
        serializer = videoSerializer(paginated_queryset, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)
                                     
    def post(self, request, format=None):
        serializer = videoSerializer(data=request.data )
        local_host_url='http://127.0.0.1:8000'
        if serializer.is_valid(): 
            ser=serializer.save()
            video=str(local_host_url)+serializer.data['video']
            width ,height= get_video_resolution(video)
            img_logo=str(local_host_url)+serializer.data['logo']
            context=serializer.data['content']
            usr=MyUser.objects.get(email=request.user.email)
            usr_img=str(local_host_url)+'/media/'+ str(usr.profile)
            
            # video, logo, new_line, context, profile, user_name
            output_file=f'media/final_video/first_output_{ser.id}.mp4'
            print(output_file)
            test_video(video, img_logo, context,
                       usr_img,  usr.name, output_file)
            # output_file2=f'media/final_video/{ser.id}.mp4'
            # command = f'ffmpeg -i {video} -i {img_logo} -i {usr_img} -filter_complex \"[0:v][1:v]overlay=10:10[bg];[bg][2:v]overlay={width-150}:8\ , drawtext=text=\'{context}\':fontsize=50:x=w-mod(t*50\,w+tw):y=h/1.2 -th/2:fontcolor=Blue:box=1:boxcolor=black@0.5"  -codec:a copy {output_file}'
            
            # os.system(command)
            # command2 = f'ffmpeg -i {output_file} -vf "drawtext=text={usr.name}":x={width-150}:y=110:fontsize=50:fontcolor=RED" -codec:a copy {output_file2}'
            # os.system(command2)
            obj=Videomodel.objects.get(id=ser.id)
            # removeable_video=Videomodel.objects.get(id=ser.id).video.path
            obj.video = f'final_video/first_output_{ser.id}.mp4'
            obj.user=request.user
            obj.save()
            ser=videoSerializer(instance=obj,many=False)
            # delete fun
            # if os.path.exists(removeable_video):
            #     os.remove(removeable_video)
            
            # if os.path.exists(output_file):
            #     os.remove(output_file)
            return Response({"status": "success", "data": ser.data}, status=status.HTTP_200_OK) 
        else:  
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  



