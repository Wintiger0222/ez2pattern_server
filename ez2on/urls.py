from django.urls import path

from . import views
app_name = 'ez2on'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    
    path('standard/<str:keys>', views.index_level, name='index_level'),
    # path('chart/<str:keys>/id=<int:song_id>/<str:difficulty>', views.detail_chart, name='detail_chart'),#차트
    path('chart/<str:keys>/<str:page_name>/<str:difficulty>', views.detail_chart, name='detail_chart'),#차트
    
    # path('standard/<str:keys>/id=<int:song_id>', views.detail_level, name='detail_level'),
    # path('standard/<str:keys>/id=<int:song_id>/<str:difficulty>', views.detail_level),
    # path('info/id=<int:song_id>/', views.detail_info),
    # path('chart/<str:file>', views.detail_chart),
    
    path('course', views.index_course, name='index_course'),
    path('course/<str:keys>', views.index_course, name='index_course'),
    # path('course/<str:keys>/id=<int:course_id>/<int:num>', views.detail_course, name='detail_course'),#코스차트
    path('course/<str:page_name>/<int:num>', views.detail_course, name='detail_course'),#코스차트

    
    # path('parameter/', views.get_post, name='parameter'),
    path('tier/<str:keys>', views.index_tier, name='index_tier'),
    # path('test/<str:keys>/<int:level>', views.index_tier, name='index_tier'),

    #API
    path('api/songs.json', views.api_song),
    path('api/allsongs.json', views.api_allsong),
    path('api/levels.json', views.api_levels),
    path('easyscore', views.easyscore),
    # path('test', views.test),
    
    # path('api/groove.json', views.api_groove),
    # path('api/<str:keys>/groove.json', views.api_groove),

    
]
