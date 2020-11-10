import os
import re

import requests
from django.template import loader
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from contextlib import closing
from translator.settings import MEDIA_ROOT

def index(request):
    template = loader.get_template('pdf_translator/index.html')
    context = {
        # 'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def read(request):
    file = request.FILES.get('trans_file', False)
    link = request.POST.get('trans_link', False)
    if link:
        with closing(requests.get(url=link, stream=True)) as resp:
            assert resp.ok and getattr(resp, 'iter_content', False)

            if "Content-Disposition" in resp.headers.keys():
                fname = re.findall("filename=(.+)", resp.headers["Content-Disposition"])[0]
            else:
                fname = link.split("/")[-1]
            content_size = int(resp.headers['content-length'])
            with open(os.path.join(MEDIA_ROOT, fname), mode='wb+') as f:
                count = 0.0
                for chunk in resp.iter_content(4096):
                    f.write(chunk)
                    count += len(chunk)
                    print("下载中： {:.2%}".format(count/content_size), end='\r')
    elif file:
        fname = file.name
        with open(os.path.join(MEDIA_ROOT, fname), 'wb+') as f:
            count = 0.0
            content_size = file.size
            for chunk in file.chunks(chunk_size=4096):
                f.write(chunk)
                count += len(chunk)
                print("下载中： {:.2%}".format(count / content_size), end='\r')
    else:
        return HttpResponseBadRequest()

    template = loader.get_template('pdf_translator/read.html')
    context = {
        # 'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def next(request):
    index = request.GET['index']
    limit = request.GET['index']
    if index is None:
        index = 0
    if limit is None:
        limit = 10