from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import os
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from files.settings import MEDIA_ROOT

fs = FileSystemStorage(location=MEDIA_ROOT)

@method_decorator(csrf_exempt,name='dispatch')
class Api(View):
    def post(self,request,*args,**kwargs):

        upload_file = request.FILES.get('file')
        # 获取文件唯一标识符
        task = request.POST.get('task_id')
        # 获取该分片所有分片中的序号
        chunk = request.POST.get('chunk',0)
        # 构成该分片唯一标识符
        filename = '%s%s' % (task, chunk)
        #　保存分片到本地
        fs.save(MEDIA_ROOT+'/{}'.format(filename),ContentFile(upload_file.read()))

        return render(request,'files.html',locals())

@method_decorator(csrf_exempt,name='dispatch')
class Up(View):

    def get(self,request,*args,**kwargs):
        task = request.GET.get('task_id')
        ext = request.GET.get('filename', '')
        upload_type = request.GET.get('type')
        if len(ext) == 0 and upload_type:
            ext = upload_type.split('/')[1]
        # 构建文件后缀名
        ext = '' if len(ext) == 0 else '.%s' % ext
        chunk = 0
        # 创建新文件
        with open(MEDIA_ROOT+'/%s%s' % (task, ext), 'wb') as target_file:
            while True:
                try:
                    filename = MEDIA_ROOT+'/%s%d' % (task, chunk)
                    # 按序打开每个分片
                    source_file = open(filename, 'rb')
                    # 读取分片内容写入新文件
                    target_file.write(source_file.read())
                    source_file.close()
                except IOError:
                    break
                chunk += 1
                # 删除该分片，节约空间
                os.remove(filename)
        return render(request,'files.html', locals())


class Zhan(View):

    def get(self,request):

        return render(request,'files.html')