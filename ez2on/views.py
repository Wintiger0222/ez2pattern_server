from django.shortcuts import get_object_or_404, render
from django.http import Http404      
from django.db.models import Case, Q, When
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator  
from .models import Song, Difficulty, Course, Pattern
import random
from datetime import date, timedelta
from django.conf import settings
from django.core import serializers
from django.http import JsonResponse, HttpResponse

# color_liner={"w":"linear-gradient(to left, #888, #fff, #888);",
#             "b":"linear-gradient(to left, rgb(0,94,159), rgb(106,232,229), rgb(0,94,159));",
#             "g":"linear-gradient(to left, rgb(4,99,17),rgb(22,203,64), #fff,rgb(22,203,64), rgb(4,99,17));"}
color_liner={"w":"linear-gradient(to left,#888,#f5f5f5);",
            "b":"linear-gradient(to left, rgb(0,94,159),#5adcff);",
            "g":"linear-gradient(to left, rgb(4,99,17),rgb(22,203,64));",
            "y":"linear-gradient(to left,#bd9739,#ffd161);",
            "r":"linear-gradient(to left,rgb(212,70,92),rgb(226,85,55));"
            }


xtMap={"4A":{
        "grid": settings.STATIC_URL+"res/grid4K.svg",
        "1":  [  0, 30,color_liner["w"],200,1.0],
        "2":  [ 30, 30,color_liner["b"],200,1.0],
        "3":  [ 60, 30,color_liner["b"],200,1.0],
        "4":  [ 90, 30,color_liner["w"],200,1.0],
        },
        "5A":{
        "grid": settings.STATIC_URL+"res/grid5K.svg",
        "1":  [  0, 24,color_liner["w"],200,1.0],
        "2":  [ 24, 24,color_liner["b"],200,1.0],
        "3":  [ 48, 24,color_liner["w"],200,1.0],
        "4":  [ 72, 24,color_liner["b"],200,1.0],
        "5":  [ 96, 24,color_liner["w"],200,1.0],
        },
        "6A":{
        "grid": settings.STATIC_URL+"res/grid6K.svg",
        "1":  [  0, 20,color_liner["w"],200,1.0],
        "2":  [ 20, 20,color_liner["b"],200,1.0],
        "3":  [ 40, 20,color_liner["w"],200,1.0],
        "4":  [ 60, 20,color_liner["w"],200,1.0],
        "5":  [ 80, 20,color_liner["b"],200,1.0],
        "6":  [ 100,20,color_liner["w"],200,1.0],
        },
        #SDVX
        "6H":{
        "grid": settings.STATIC_URL+"res/grid4K.svg",
        "1":  [  0, 60,color_liner["r"],100,1.0],
        "2":  [ 1,  28,color_liner["w"],200,0.7],
        "3":  [ 31, 28,color_liner["w"],200,0.7],
        "4":  [ 61, 28,color_liner["w"],200,0.7],
        "5":  [ 91, 28,color_liner["w"],200,0.7],
        "6":  [ 60, 60,color_liner["r"],100,1.0],
        },
        "7A":{
        "grid": settings.STATIC_URL+"res/grid7K.svg",
        "1":  [  0, 17,color_liner["w"],200,1.0],
        "2":  [ 17, 15,color_liner["b"],200,1.0],
        "3":  [ 32, 17,color_liner["w"],200,1.0],
        "4":  [ 49, 22,color_liner["y"],200,1.0],
        "5":  [ 71, 17,color_liner["w"],200,1.0],
        "6":  [ 88, 15,color_liner["b"],200,1.0],
        "7":  [ 103,17,color_liner["w"],200,1.0],
        },
        #8키
        "8A":{
        "grid": settings.STATIC_URL+"res/grid8K.svg",
        "1":  [  0, 15,color_liner["w"],200,1.0],
        "2":  [ 15, 15,color_liner["b"],200,1.0],
        "3":  [ 30, 15,color_liner["w"],200,1.0],
        "4":  [ 45, 15,color_liner["b"],200,1.0],
        "5":  [ 60, 15,color_liner["b"],200,1.0],
        "6":  [ 75, 15,color_liner["w"],200,1.0],
        "7":  [ 90, 15,color_liner["b"],200,1.0],
        "8":  [ 105,15,color_liner["w"],200,1.0],
        },
        "8B":{
        "grid": settings.STATIC_URL+"res/grid8K.svg",
        "1":  [  0, 15,color_liner["w"],200,1.0],
        "2":  [ 15, 15,color_liner["b"],200,1.0],
        "3":  [ 30, 15,color_liner["w"],200,1.0],
        "4":  [ 45, 15,color_liner["b"],200,1.0],
        "5":  [ 60, 15,color_liner["w"],200,1.0],
        "6":  [ 75, 15,color_liner["b"],200,1.0],
        "7":  [ 90, 15,color_liner["w"],200,1.0],
        "8":  [ 105,15,color_liner["b"],200,1.0],
        },
        "8C":{
        "grid": settings.STATIC_URL+"res/grid8K.svg",
        "1":  [  0, 15,color_liner["g"],200,1.0],
        "2":  [ 15, 15,color_liner["w"],200,1.0],
        "3":  [ 30, 15,color_liner["b"],200,1.0],
        "4":  [ 45, 15,color_liner["w"],200,1.0],
        "5":  [ 60, 15,color_liner["w"],200,1.0],
        "6":  [ 75, 15,color_liner["b"],200,1.0],
        "7":  [ 90, 15,color_liner["w"],200,1.0],
        "8":  [ 105,15,color_liner["g"],200,1.0],
        },
        "8D":{
        "grid": settings.STATIC_URL+"res/grid8K.svg",
        "1":  [  0, 15,color_liner["g"],200,1.0],
        "2":  [ 15, 15,color_liner["w"],200,1.0],
        "3":  [ 30, 15,color_liner["b"],200,1.0],
        "4":  [ 45, 15,color_liner["w"],200,1.0],
        "5":  [ 60, 15,color_liner["g"],200,1.0],
        "6":  [ 75, 15,color_liner["w"],200,1.0],
        "7":  [ 90, 15,color_liner["b"],200,1.0],
        "8":  [ 105,15,color_liner["w"],200,1.0],
        },
        "8E":{
        "grid": settings.STATIC_URL+"res/grid8K.svg",
        "1":  [  0, 15,color_liner["w"],200,1.0],
        "2":  [ 15, 15,color_liner["b"],200,1.0],
        "3":  [ 30, 15,color_liner["w"],200,1.0],
        "4":  [ 45, 15,color_liner["g"],200,1.0],
        "5":  [ 60, 15,color_liner["g"],200,1.0],
        "6":  [ 75, 15,color_liner["w"],200,1.0],
        "7":  [ 90, 15,color_liner["b"],200,1.0],
        "8":  [ 105,15,color_liner["w"],200,1.0],
        },
        "8F":{
        "grid": settings.STATIC_URL+"res/grid8K.svg",
        "1":  [  0, 15,color_liner["g"],200,1.0],
        "2":  [ 15, 15,color_liner["w"],200,1.0],
        "3":  [ 30, 15,color_liner["b"],200,1.0],
        "4":  [ 45, 15,color_liner["w"],200,1.0],
        "5":  [ 60, 15,color_liner["b"],200,1.0],
        "6":  [ 75, 15,color_liner["w"],200,1.0],
        "7":  [ 90, 15,color_liner["b"],200,1.0],
        "8":  [ 105,15,color_liner["w"],200,1.0],
        },
        "8G":{
        "grid": settings.STATIC_URL+"res/grid8K.svg",
        "1":  [  0, 15,color_liner["w"],200,1.0],
        "2":  [ 15, 15,color_liner["b"],200,1.0],
        "3":  [ 30, 15,color_liner["w"],200,1.0],
        "4":  [ 45, 15,color_liner["b"],200,1.0],
        "5":  [ 60, 15,color_liner["w"],200,1.0],
        "6":  [ 75, 15,color_liner["b"],200,1.0],
        "7":  [ 90, 15,color_liner["w"],200,1.0],
        "8":  [ 105,15,color_liner["g"],200,1.0],
        },
        "8H":{#DJMAX
        "grid": settings.STATIC_URL+"res/grid6K.svg",
        "1":  [  0, 60,color_liner["r"],100,1.0],
        "2":  [  0, 20,color_liner["w"],200,0.7],
        "3":  [ 20, 20,color_liner["b"],200,0.7],
        "4":  [ 40, 18,color_liner["w"],200,0.7],
        "5":  [ 62, 18,color_liner["w"],200,0.7],
        "6":  [ 80, 20,color_liner["b"],200,0.7],
        "7":  [ 100,20,color_liner["w"],200,0.7],
        "8":  [ 60, 60,color_liner["r"],100,1.0],
        },
        "8I":{#AE23S
        "grid": settings.STATIC_URL+"res/grid6K.svg",
        "1":  [  0, 20,color_liner["w"],200,0.7],
        "2":  [ 20, 20,color_liner["b"],200,0.7],
        "3":  [ 40, 18,color_liner["w"],200,0.7],
        "4":  [ 0,  60,color_liner["r"],100,1.0],
        "5":  [ 60, 60,color_liner["r"],100,1.0],
        "6":  [ 62, 18,color_liner["w"],200,0.7],
        "7":  [ 80, 20,color_liner["b"],200,0.7],
        "8":  [ 100,20,color_liner["w"],200,0.7],
        },
        "TRIGER":{#AE23S
        "A":  [ 0,  60,color_liner["b"],50,0.3],
        "B":  [ 60, 60,color_liner["b"],50,0.3],
        },
    }
#키 순서처리
def keyorder(request,key_val):
    if   key_val==4: key_noran="1234"
    elif key_val==5: key_noran="12345"
    elif key_val==6: key_noran="123456"
    elif key_val==7: key_noran="1234567"
    elif key_val==8: key_noran="12345678"
    key_mirror = key_noran[::-1]
    key_random= list(key_noran)
    random.shuffle(key_random)
    key_random=''.join(key_random)

    #플립랜덤 구현
    if   key_val==4: 
        key_left="12"
        key_center=""
        key_right="34"
    elif key_val==5: 
        key_left="12"
        key_center="3"
        key_right="45"
    elif key_val==6: 
        key_left="123"
        key_center=""
        key_right="456"
    elif key_val==7: 
        key_left="123"
        key_center="4"
        key_right="567"
    elif key_val==8: 
        key_left="1234"
        key_center=""
        key_right="5678"
    key_left= list(key_left)
    key_right= list(key_right)
    random.shuffle(key_left)
    random.shuffle(key_right)
    key_left=''.join(key_left)
    key_right=''.join(key_right)

    key_frandom=key_left+key_center+key_right
    key_mfrandom=key_right+key_center+key_left

    #최종 키순서값
    key_order = request.GET.get('order', key_noran) 

    return key_order, key_mirror, key_random, key_frandom, key_mfrandom

#CSS 처리
def innerCSSMake(key_val, key_order, key_type):
    key_char=str(key_val)+key_type
    innerCSS=".bar-note {background-image: url(\""+xtMap[key_char]["grid"]+"\");}\n \
                .note {background: linear-gradient(to left,#888,#f5f5f5); z-index:100;}\n"

    for i in range(key_val):
        innerCSS+=".note-"+str(i)+"{margin-left:"+str(xtMap[key_char][key_order[i]][0])+"px;"+\
                                "width:"+str(xtMap[key_char][key_order[i]][1])+"px;"+\
                                "background:"+xtMap[key_char][key_order[i]][2]+";"+\
                                "z-index:"+str(xtMap[key_char][key_order[i]][3])+";"+\
                                "opacity:"+str(xtMap[key_char][key_order[i]][4])+";}\n"
        
    innerCSS+=".note-A{margin-left:"+str(xtMap["TRIGER"]["A"][0])+"px;"+\
                                "width:"+str(xtMap["TRIGER"]["A"][1])+"px;"+\
                                "background:"+xtMap["TRIGER"]["A"][2]+";"+\
                                "z-index:"+str(xtMap["TRIGER"]["A"][3])+";"+\
                                "opacity:"+str(xtMap["TRIGER"]["A"][4])+";}\n"
    innerCSS+=".note-B{margin-left:"+str(xtMap["TRIGER"]["B"][0])+"px;"+\
                                "width:"+str(xtMap["TRIGER"]["B"][1])+"px;"+\
                                "background:"+xtMap["TRIGER"]["B"][2]+";"+\
                                "z-index:"+str(xtMap["TRIGER"]["B"][3])+";"+\
                                "opacity:"+str(xtMap["TRIGER"]["B"][4])+";}\n"

    return innerCSS

def main_page(request):
    page_info={
        'title': "EZ2PATTERN",
        'description': "EZ2PATTERN",
        'canonical_url' : request.build_absolute_uri(request.path),
        'keyword':  "EZ2ON",
        'game':"ez2on",
        'debug':settings.DEBUG
    }
    context = {
        'page_info': page_info
    }
    return render(request,'ez2on/main.html', context)

def index_level(request, keys="4S"):

    # GET 값 받아오기
    page = request.GET.get('page', '1')  
    category = request.GET.get('category', 'ALL') 
    level = request.GET.get('level', 'ALL') 
    
    #유효성 검사
    if len(page)>3: raise Http404()
    if len(category)>5: raise Http404()
    if len(level)>4: raise Http404()
    if keys not in ['4B', '4S', '5B', '5S', '6B', '6S', '8B', '8S']:       
        raise Http404()

    #DB 불러오기
    song_list = Difficulty.objects.filter(key=keys).order_by('-SHDmix_level', '-HDmix_level', 'song__name_kr_order')
    
    #카테고리 처리
    page_text = ""
    if category!="ALL":
        if category == "NEW":
            song_list = song_list.filter(song__update_date__range=[date.today() - timedelta(days=60), date.today()]).order_by('-song__update_date','song__name_kr_order')
            page_text += "category="+category+"&"
        else:
            song_list = song_list.filter(song__category=category)
            page_text += "category="+category+"&"
    
    #레벨 처리
    level_int=0
    if level!="ALL":
       song_list = song_list.filter(Q(EZmix_level=level) | Q(NMmix_level=level) | Q(HDmix_level=level) | Q(SHDmix_level=level)).order_by('song__name_kr_order')
       page_text += "level="+level+"&"
       level_int= int(level)

    #페이지 자르기
    paginator = Paginator(song_list, 40)  
    page_obj = paginator.get_page(page)
    num_page = paginator.num_pages
      
    #페이지 제목
    if "B" in keys:
        title_sub = keys.replace('B','K')+" BASIC"
    else:
        title_sub = keys.replace('S','K')+" STANDARD"
  
    page_info={
        'title': "EZ2PATTERN - "+ title_sub,
        'description': "EZ2PATTERN - "+ title_sub,
        'canonical_url' : request.build_absolute_uri(request.path),
        'keyword':  "EZ2ON",
        'game':"ez2on",
        'debug':settings.DEBUG
    }
    context = {
        'page_info': page_info,

        'song_list': page_obj,
        
        'key':keys,
        'page_text':page_text,
        'num_page':num_page,
        'level':level_int,
    }
    return render(request,'ez2on/index_level.html',context)


def index_course(request, keys="4K"):
    page = request.GET.get('page', '1')

    #유효성검사
    if len(page)>3: raise Http404()
    if keys not in ['4K', '5K', '6K', '8K', 'SP']:       
        raise Http404()

    #페이지 처리 #코스는 아직 많지 않아 페이지가 제대로 구현되어있지 않음
    
    course_list = Course.objects.filter(key=keys).filter(deleted=0).order_by('ingame_order')
    # paginator = Paginator(course_list, 20) 
    # page_obj = paginator.get_page(page)

    page_info={
        'title': "EZ2PATTERN - " + keys + " COURSE",
        'description': "EZ2PATTERN - " + keys + " COURSE",
        'canonical_url' : request.build_absolute_uri(request.path),
        'keyword':  "EZ2ON",
        'game':"ez2on",
        'debug':settings.DEBUG
    }
    context = {
        'page_info': page_info,
        # 'course_list': page_obj,
        'course_list': course_list,
        'key':keys,
    }
    return render(request,'ez2on/index_course.html',context)


def detail_chart(request, page_name, song_id=0, keys="4K", difficulty="SHD"):
    if song_id != 0:
        song = get_object_or_404(Song, pk=song_id)
    else:
        song = get_object_or_404(Song, page_name=page_name)
        song_id = song.id

    #DB에서 패턴 데이터 불러오기
    pattern_data = None  
    try:
        if  difficulty!="SHD": pattern_data = song.pattern_set.get(key=keys.replace("B","S"), difficulty=difficulty)
        elif difficulty!="HD": pattern_data = song.pattern_set.get(key=keys.replace("B","S"), difficulty=difficulty)
        elif difficulty!="NM": pattern_data = song.pattern_set.get(key=keys.replace("B","S"), difficulty=difficulty)
        # elif difficulty=="EZ":  pattern_data = song.pattern_set.get(key=keys, difficulty=difficulty)  
        else:  pattern_data = song.pattern_set.get(key=keys, difficulty=difficulty)  
    except ObjectDoesNotExist:
        pattern_data = None  

    # 패턴 파일 읽어오기
    file_name="./chart/ez2on/"
    if  difficulty=="SHD": file_name+= str(song_id)+"/"+difficulty+"."+keys.replace("B","K").replace("S","K")
    elif difficulty=="HD": file_name+= str(song_id)+"/"+difficulty+"."+keys.replace("B","K").replace("S","K")
    elif difficulty=="NM": file_name+= str(song_id)+"/"+difficulty+"."+keys.replace("B","K").replace("S","K")
    # elif difficulty=="EZ": file_name+= str(song_id)+"/"+difficulty+"."+keys
    # else: raise Http404()
    else:                file_name+= str(song_id)+"/"+difficulty+"."+keys
    with open(file_name+".html", "r", encoding='utf8') as p:
        innerHTML = p.read()

    #키순서 처리
    key_val=int(keys.replace("B","").replace("S","").replace("X","").replace("K",""))
    (key_order, key_mirror, key_random, key_frandom, key_mfrandom, )=keyorder(request,key_val)
    if len(key_order)!=key_val: raise Http404()
    
    
    if len(difficulty)>10: raise Http404()

    #CSS 처리
    key_type = request.GET.get('type', "A") 
    innerCSS=innerCSSMake(key_val,key_order,key_type)

    page_info={
        'title': "EZ2PATTERN - " + song.name_kr + " " + keys + " " + difficulty,
        'description': "EZ2PATTERN - " + song.name_kr + " " + keys + " " + difficulty,
        'canonical_url' : request.build_absolute_uri(request.path),
        'keyword':  "EZ2ON",
        'game':"ez2on",
        'debug':settings.DEBUG
    }

    context={
        'page_info': page_info,

        'key_mirror':key_mirror,
        'key_random':key_random,
        'key_frandom':key_frandom,
        'key_mfrandom':key_mfrandom,
        'key_order':key_order,
        'key_type':key_type,

        'song': song,
        
        'keys': keys,
        'difficulty': difficulty,
        'pattern_data': pattern_data,

        'innerHTML' : innerHTML,
        'innerCSS'  : innerCSS,

        'course' : False,
    }
    return render(request, 'ez2on/detail_chart.html', context)


def detail_course(request, page_name, num, keys="4K", course_id=0):
    if course_id != 0:
        course = get_object_or_404(Course, pk=course_id)
    else:
        course = get_object_or_404(Course, page_name=page_name)
        course_id = course.id
    if   num == 1:
        song_id = course.song1_id
        song_key = course.song_key1
    elif num == 2:
        song_id = course.song2_id
        song_key = course.song_key2
    elif num == 3:
        song_id = course.song3_id
        song_key = course.song_key3
    else:         
        song_id = course.song4_id
        song_key = course.song_key4
    song = get_object_or_404(Song, pk=song_id)
    try:
        pattern_data = song.pattern_set.get(key=song_key, difficulty=course.file_name)
    except ObjectDoesNotExist:
        pattern_data = None  
    
    #키순서 처리
    key_val=int(song_key.replace("B","").replace("S","").replace("X","").replace("K",""))
    (key_order, key_mirror, key_random, key_frandom, key_mfrandom, )=keyorder(request,key_val)
    if len(key_order)!=key_val: raise Http404()

    #HTML 파일 읽어오기
    file_name= "./chart/ez2on/"+str(song_id)+"/"+str(course.file_name)+"."+song_key
    with open(file_name+".html", "r", encoding='utf8') as p:
        innerHTML = p.read()

    #CSS 처리
    key_type = request.GET.get('type', "A") 
    innerCSS=innerCSSMake(key_val,key_order,key_type)

    #제목 처리 
    page_info={
        'title': "EZ2PATTERN - "+ song.name_kr + " " + course.name_kr +  " " + course.key,
        'description': "EZ2PATTERN - "+ song.name_kr + " " + course.name_kr +  " " + course.key,
        'canonical_url' : request.build_absolute_uri(request.path),
        'keyword':  "EZ2ON",
        'game':"ez2on",
        'debug':settings.DEBUG
    }


    context={
        'page_info': page_info,

        'key_mirror':key_mirror,
        'key_random':key_random,
        'key_frandom':key_frandom,
        'key_mfrandom':key_mfrandom,
        'key_order':key_order,
        'key_type':key_type,

        'song': song,
        
        'keys': song_key,
        'difficulty': course.file_name,
        'pattern_data': pattern_data,

        'innerHTML' : innerHTML,
        'innerCSS'  : innerCSS,

        'course' : True,
    }
    return render(request, 'ez2on/detail_chart.html', context)


    
def index_tier(request, keys="4K"):

    #GET 처리
    level_char = request.GET.get('level', '16') 
    page = request.GET.get('page', '1')  
    category = request.GET.get('category', 'ALL') 

    level= int(level_char)

    # sublevel_char = request.GET.get('sub', 'ALL') 
    # sublevel = request.GET.get('sublevel', 'A') 

    #유효성 검사
    if len(page)>3: raise Http404()
    if len(category)>5: raise Http404()
    if len(level_char)>4: raise Http404()
    if keys not in ['4K', '5K', '6K', '7K', '8K']:       
        raise Http404()

    temp_text1=keys.replace("K","X")
    temp_text2=keys.replace("K","S")
    temp_text3=keys.replace("K","B")
    song_list = Pattern.objects.filter(Q(key=keys) | Q(key=temp_text1) | Q(key=temp_text2) | Q(key=temp_text3)).filter(level=level)
    
    # custom_list = ["S+", "S", "A", "B", "C", "D", "E", "F" , "0"]
    # order = Case(*[When(sublevel=sublevel, then=pos) for pos, sublevel in enumerate(custom_list)])
    # song_list = song_list.order_by(order)

    # song_list = song_list.filter(sublevel=sublevel)

    song_list_0 = song_list.filter(sublevel="0")
    song_list_1 = song_list.filter(sublevel="S+")
    song_list_2 = song_list.filter(sublevel="S")
    song_list_3 = song_list.filter(sublevel="A")
    song_list_4 = song_list.filter(sublevel="B")
    song_list_5 = song_list.filter(sublevel="C")
    song_list_6 = song_list.filter(sublevel="D")
    song_list_7 = song_list.filter(sublevel="E")
    song_list_8 = song_list.filter(sublevel="F")

    page_text=""
    page_info={
        'title': "EZ2PATTERN - " +  keys + " TIER",
        'description': "EZ2PATTERN - " +  keys + " TIER",
        'canonical_url' : request.build_absolute_uri(request.path),
        'keyword':  "EZ2ON",
        'game':"ez2on",
        'debug':settings.DEBUG
    }
    context = {
        'page_info': page_info,

        'song_list': song_list,
        'song_list_0': song_list_0,
        'song_list_1': song_list_1,
        'song_list_2': song_list_2,
        'song_list_3': song_list_3,
        'song_list_4': song_list_4,
        'song_list_5': song_list_5,
        'song_list_6': song_list_6,
        'song_list_7': song_list_7,
        'song_list_8': song_list_8,
        
        'level':level,
        'key':keys,
        'page_text':page_text,
        'num_page':"1",
    }
    return render(request,'ez2on/index_tier.html',context)

#############################API PART

def api_song(request):
    songs = Song.objects.exclude(deleted=True).exclude(category="ALL").order_by('name_kr_order')
    songs_json = []

    new_order = 0
    for song in songs:
        new_order=new_order+1
        songs_json.append(
            {
                'id':song.id,
                'name':song.name_kr,
                "composer":song.composer,
                "category":song.category,
                'order':new_order,#song.name_kr_order,
                "min_bpm":song.min_bpm,
                "max_bpm":song.max_bpm,
                "playtime":song.playtime,
                "update_date":song.update_date,
                # "deleted":song.deleted
            }
        )
    songs_json = sorted(songs_json, key=lambda song: (song['id']))

    return JsonResponse(songs_json, safe=False)


def api_allsong(request):
    songs = Song.objects.all()
    songs_json = []

    for song in songs:
        songs_json.append(
            {
                'id':song.id,
                'name':song.name_kr,
                "composer":song.composer,
                "category":song.category,
                'order':song.name_kr_order,
                "min_bpm":song.min_bpm,
                "max_bpm":song.max_bpm,
                "playtime":song.playtime,
                "update_date":song.update_date,
                "deleted":song.deleted
            }
        )

    return JsonResponse(songs_json, safe=False)

def api_levels(request):
    key = request.GET.get('key', 'ALL') 
    if key!="ALL":
        songs = Difficulty.objects.filter(key=key)
    else:
        songs = Difficulty.objects.all()
    songs_json = []

    for song in songs:
        songs_json.append(
            {
                'song_id':song.song_id,
                'key':song.key,
                 'EZ' :song.EZmix_level,
                 'NM':song.NMmix_level,
                 'HD':song.HDmix_level,
                 'SHD':song.SHDmix_level,
            }
        )

    return JsonResponse(songs_json, safe=False)

def easyscore(request):
    return render(request,'ez2on/easy_score.html')

def api_groove(request):
    songs = Song.objects.exclude(deleted=True).exclude(category="ALL").order_by('name_kr_order')
    patterns = Pattern.objects.all()

    #make order list
    songs_data = {}
    patterns_json = []
    new_order = 0
    for song in songs:
        new_order=new_order+1
        songs_data[song.id]=[new_order,song.name_kr]
    
    for pattern in patterns:
            patterns_json.append(
            {
                'id':pattern.song_id,
                'key':pattern.key,
                'difficulty':pattern.difficulty,
                'name':songs_data[pattern.song_id][1],
                'order':songs_data[pattern.song_id][0],
                "notes":pattern.notes,
                "notes_groove":pattern.notes_groove,
                "climax_groove":pattern.climax_groove,
                "multi_groove":pattern.multi_groove,
                "long_groove":pattern.long_groove,
                "mayhem_groove":pattern.mayhem_groove
            }
        )

    return JsonResponse(patterns_json, safe=False)