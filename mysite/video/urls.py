from django.urls import path
from . import views

app_name='video'

urlpatterns=[
    path('',views.all_film,name='all_film'),
    path('<str:kinds>/',views.all_film,name='all_film'),
    path('ajax/<str:kinds>',views.ajax_handle,name='ajax_handle'),
    path('search/<search>/',views.search_film,name='search_film'),
    path('search/ajax',views.ajax_search,name='ajax_search'),
    path('play/<str:videoId>/<int:Id>/<str:kinds>/',views.play_video,name='play_video'),
    path('<str:key>/play/<str:videoId>/<int:Id>/<str:kinds>/',views.play_video,name='play_video'),
    path('<str:key1>/<str:key>/play/<str:videoId>/<int:Id>/<str:kinds>/',views.play_video,name='play_video'),
    path('logout/done/',views.log_out,name='log_out'),
]