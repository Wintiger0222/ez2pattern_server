from django.urls import path

from . import views
app_name = 'djmax'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    
    path('freestyle/<str:keys>', views.index_level, name='index_level'),
    path('chart/<str:keys>/<str:page_name>/<str:difficulty>', views.detail_chart, name='detail_chart'),#차트
    
    # path('parameter/', views.get_post, name='parameter'),
    # path('tier/<str:keys>', views.index_tier, name='index_tier'),
    # path('test/<str:keys>/<int:level>', views.index_tier, name='index_tier'),

    
]
