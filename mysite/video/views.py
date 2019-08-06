from django.shortcuts import render,redirect,reverse,get_object_or_404
from .models import Film
from django.http import JsonResponse
# Create your views here.

num=20
ajax_search_films=[] #承接搜尋到的Film物件(20~)
num1=0

def all_film(request,kinds=None):
    if request.POST:
        data={}
        data['search']=request.POST['search_input']
        url=reverse('video:search_film',kwargs=data)
        return redirect(url)
    else:
        films=Film.objects.filter(kind='全部').order_by('-publish')[0:20]
        film=Film.objects.filter(kind='全部').get(id=1)
        movie=Film.objects.filter(kind='電影').get(id=21)
        knowledge=Film.objects.filter(kind='知識').get(id=41)
        sport=Film.objects.filter(kind='運動').get(id=61)
        basketball=Film.objects.filter(kind='籃球').get(id=81)
        entertainment=Film.objects.filter(kind='娛樂').get(id=101)
        life=Film.objects.filter(kind='生活').get(id=121)
        political=Film.objects.filter(kind='政治').get(id=141)
        food=Film.objects.filter(kind='食物').get(id=161)
        technology=Film.objects.filter(kind='科技').get(id=181)
        global num
        num=20
        if kinds:
            films=Film.objects.filter(kind=kinds).order_by('-publish')[0:20]
            num=20
        rep=render(request,'video/index.html',{'films':films,
                                                                                                'film':film,
                                                                                                'movie':movie,
                                                                                                'knowledge':knowledge,
                                                                                                'sport':sport,
                                                                                                'basketball':basketball,
                                                                                                'entertainment':entertainment,
                                                                                                'life':life,
                                                                                                'political':political,
                                                                                                'food':food,
                                                                                                'technology':technology,
                                                                                                'film1':films[0]})
        rep['Cache-Control']='no-store, no-cache, must-revalidate'
        rep['Expires']='Mon, 26 Jul 1990 05:00:00 GMT'
        return rep
def ajax_handle(request,kinds):
    global num
    films=Film.objects.filter(kind=kinds).order_by('-publish')[num:num+4]
    films_all=Film.objects.filter(kind=kinds).order_by('-publish')
    data={}
    data['items']=[]
    data['num']=num
    for i in range(0,4):
        item={'image':films[i].image_url,'title':films[i].title,'view':films[i].views,'videoId':films[i].video_id,'id':films[i].id,'kind':films[i].kind}
        data['items'].append(item)
    num+=4
    if num>=films_all.count():
        data['num']=-1
        num=20
    return JsonResponse(data)
def search_film(request,search):
    films=Film.objects.filter(title__icontains=search)
    film=Film.objects.filter(kind='全部').get(id=1)
    movie=Film.objects.filter(kind='電影').get(id=21)
    knowledge=Film.objects.filter(kind='知識').get(id=41)
    sport=Film.objects.filter(kind='運動').get(id=61)
    basketball=Film.objects.filter(kind='籃球').get(id=81)
    entertainment=Film.objects.filter(kind='娛樂').get(id=101)
    life=Film.objects.filter(kind='生活').get(id=121)
    political=Film.objects.filter(kind='政治').get(id=141)
    food=Film.objects.filter(kind='食物').get(id=161)
    technology=Film.objects.filter(kind='科技').get(id=181)
    if films.count()<20:
        rep=render(request,'video/search.html',{'films':films,
                                                                                                'film':film,
                                                                                                'movie':movie,
                                                                                                'knowledge':knowledge,
                                                                                                'sport':sport,
                                                                                                'basketball':basketball,
                                                                                                'entertainment':entertainment,
                                                                                                'life':life,
                                                                                                'political':political,
                                                                                                'food':food,
                                                                                                'technology':technology})
        rep['Cache-Control']='no-store, no-cache, must-revalidate'
        rep['Expires']='Mon, 26 Jul 1990 05:00:00 GMT'
        return rep
    else:
        global ajax_search_films
        ajax_search_films=films[20:]
        start_ajax=True
        global num1
        num1=0
        rep=render(request,'video/search.html',{'films':films[0:20],
                                                                                                'film':film,
                                                                                                'movie':movie,
                                                                                                'knowledge':knowledge,
                                                                                                'sport':sport,
                                                                                                'basketball':basketball,
                                                                                                'entertainment':entertainment,
                                                                                                'life':life,
                                                                                                'political':political,
                                                                                                'food':food,
                                                                                                'technology':technology,
                                                                                                'start_ajax':start_ajax})
        rep['Cache-Control']='no-store, no-cache, must-revalidate'
        rep['Expires']='Mon, 26 Jul 1990 05:00:00 GMT'
        return rep
def ajax_search(request):
    global num1
    if ajax_search_films.count()%8:
        if num1>=(ajax_search_films.count()-(ajax_search_films.count()%8)):
            films=ajax_search_films[num1:]
            data={}
            data['items']=[]
            data['num1']=num1
            for i in range(0,films.count()):
                item={'image':films[i].image_url,'title':films[i].title,'view':films[i].views,'videoId':films[i].video_id,'id':films[i].id,'kind':films[i].kind}
                data['items'].append(item)
            data['num1']=-1
            num1=0
            return JsonResponse(data)
        films=ajax_search_films[num1:num1+8]
        data={}
        data['items']=[]
        data['num1']=num1
        for i in range(0,8):
            item={'image':films[i].image_url,'title':films[i].title,'view':films[i].views,'videoId':films[i].video_id,'id':films[i].id,'kind':films[i].kind}
            data['items'].append(item)
        num1+=8
        return JsonResponse(data)
    else:
        films=ajax_search_films[num1:num1+8]
        data={}
        data['items']=[]
        data['num1']=num1
        for i in range(0,8):
            item={'image':films[i].image_url,'title':films[i].title,'view':films[i].views,'videoId':films[i].video_id,'id':films[i].id,'kind':films[i].kind}
            data['items'].append(item)
        num1+=8
        if num1>=ajax_search_films.count():
            data['num1']=-1
            num1=0
        return JsonResponse(data)
def play_video(request,videoId,Id,kinds,key=None,key1=None):
    film=get_object_or_404(Film,video_id=videoId,id=Id)
    film.views+=1
    film.save()
    films=Film.objects.exclude(video_id=videoId,id=Id).filter(kind=kinds).order_by('?')[0:20]
    rep=render(request,'video/play.html',{'film':film,'films':films})
    rep['Cache-Control']='no-store, no-cache, must-revalidate'
    rep['Expires']='Mon, 26 Jul 1990 05:00:00 GMT'
    return rep