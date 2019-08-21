from django.shortcuts import render,redirect,reverse,get_object_or_404
from .models import Film,user_filmlist,Comment
from django.http import JsonResponse
from django.contrib.auth import logout,login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import CommentForm
# Create your views here.

ajax_search_films=[] #承接搜尋到的Film物件(20~)

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
    films=Film.objects.filter(kind=kinds).order_by('-publish')[20:]
    data={}
    data['items']=[]
    if 'sessionid' in request.COOKIES:
        data['mylove']=True
    else:
        data['mylove']=False
    for i in range(0,films.count()):
        item={'image':films[i].image_url,'title':films[i].title,'view':films[i].views,'videoId':films[i].video_id,'id':films[i].id,'kind':films[i].kind}
        data['items'].append(item)
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
    global ajax_search_films
    if films.count()<=20:
        ajax_search_films=[]
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
        ajax_search_films=films[20:]
        start_ajax=True
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
    if not ajax_search_films:
        data={}
        data['null']=1
        rep=JsonResponse(data)
        rep['Cache-Control']='no-store, no-cache, must-revalidate'
        rep['Expires']='Mon, 26 Jul 1990 05:00:00 GMT'
        return rep
    else:
        films=ajax_search_films
        data={}
        data['items']=[]
        data['sum']=films.count()
        data['null']=0
        if 'sessionid' in request.COOKIES:
            data['mylove']=True
        else:
            data['mylove']=False
        for i in range(0,films.count()):
            item={'image':films[i].image_url,'title':films[i].title,'view':films[i].views,'videoId':films[i].video_id,'id':films[i].id,'kind':films[i].kind}
            data['items'].append(item)
        rep=JsonResponse(data)
        rep['Cache-Control']='no-store, no-cache, must-revalidate'
        rep['Expires']='Mon, 26 Jul 1990 05:00:00 GMT'
        return rep
def play_video(request,videoId,Id,kinds):
    film=get_object_or_404(Film,video_id=videoId,id=Id)
    film.views+=1
    film.save()
    films=Film.objects.exclude(video_id=videoId,id=Id).filter(kind=kinds).order_by('?')[0:20]
    new_comment=None
    if request.method=='POST':
        if request.POST.get('id_comment',False):
            comment=Comment.objects.get(pk=request.POST['id_comment'])
            comment.delete()
        else:
            comment_form=CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment=comment_form.save(commit=False)
                new_comment.film=film
                new_comment.name=request.user.first_name
                new_comment.save()
    else:
        comment_form=CommentForm()
    comments=film.comments.filter(published=True)
    rep=render(request,'video/play.html',{'film':film,'films':films,'comments':comments})
    rep['Cache-Control']='no-store, no-cache, must-revalidate'
    rep['Expires']='Mon, 26 Jul 1990 05:00:00 GMT'
    return rep
@login_required
def ajax_love(request,film_id,user_id):
    uf=user_filmlist.objects.all()
    if  not uf.count():
        user_filmlist.objects.create(userId=user_id,filmList='')
    try:
        user_obj=user_filmlist.objects.get(userId=user_id)
    except ObjectDoesNotExist:
        user_obj=user_filmlist.objects.create(userId=user_id,filmList='')
    request.session['user_info']={}
    request.session['user_info'][user_id]=film_id
    request.session.modified = True
    user_obj.filmList+=request.session['user_info'][user_id]+','
    user_obj.save()
    data={}
    data['success']=True
    rep=JsonResponse(data)
    rep['Cache-Control']='no-store, no-cache, must-revalidate'
    rep['Expires']='Mon, 26 Jul 1990 05:00:00 GMT'
    return rep
@login_required
def log_out(request):
    logout(request)
    return redirect(reverse('video:all_film'))
@login_required
def mylist(request,user_id):
    film_list=[]
    try:
        user_obj=user_filmlist.objects.get(userId=str(user_id))
    except ObjectDoesNotExist:
        user_obj=None
    if user_obj != None:
        film_id_list=user_obj.filmList.split(',')
        film_id_list.remove('')
        film_id_list=list(set(film_id_list))
        for f in film_id_list:
            try:
                film=Film.objects.get(pk=int(f))
            except ObjectDoesNotExist:
                continue
            film_list.append(film)
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
    rep=render(request,'video/list.html',{'film_list':film_list,
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
@login_required
def ajax_delete(request,film_id,user_id):
    user_obj=user_filmlist.objects.get(userId=str(user_id))
    film_id_list=user_obj.filmList.split(',')
    film_id_list.remove(film_id)
    user_obj.filmList=','.join(film_id_list)
    user_obj.save()
    data={}
    data['delete']=True
    rep=JsonResponse(data)
    rep['Cache-Control']='no-store, no-cache, must-revalidate'
    rep['Expires']='Mon, 26 Jul 1990 05:00:00 GMT'
    return rep