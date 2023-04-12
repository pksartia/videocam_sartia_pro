from rest_framework import serializers  
from .models import Videomodel  
from users.models import MyUser
  
class videoSerializer(serializers.ModelSerializer):
    class Meta:  
        model = Videomodel  
        fields = ('id','video','content','logo')

    def create(self,validated_data,*args, **kwargs):
        video = Videomodel.objects.create(video=self.validated_data['video'],
                content=self.validated_data['content'],logo=self.validated_data['logo']
                )
        return video
    
    def paginate_queryset(self, queryset, request, view=None):
        paginator = self.paginator
        if paginator is None:
            return None

        return paginator.paginate_queryset(queryset, request, view=view)
    
    def get_file_abs_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url)