import requests
from django.http import JsonResponse, HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('pdf_translator/index.html')
    context = {
        # 'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def read(request):
    link = request.POST.get('trans_link', False)
    file = request.FILES.get('trans_file', False)
    if link:
        req = requests.get(url=link, stream=True)
        assert req.ok and getattr(req, 'iter_content', False)
        with open('tmp.pdf', mode='wb+') as f:
            for chunk in req.iter_content(4096):
                f.write(chunk)
    elif file:
        print("file", file, type(file))
    else:
        file = "/home/welsun/下载/Tang_Non-Contact_Heart_Rate_CVPR_2018_paper.pdf"
        print(3)

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