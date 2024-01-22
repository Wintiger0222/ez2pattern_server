from django.shortcuts import get_object_or_404, render
from django.http import Http404      
from django.db.models import Case, Q, When
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator  
from .models import Song, Difficulty, Pattern
import random
from datetime import date, timedelta
from django.conf import settings


# color_liner={"w":"linear-gradient(to left, #888, #fff, #888);",
#             "b":"linear-gradient(to left, rgb(0,94,159), rgb(106,232,229), rgb(0,94,159));",
#             "g":"linear-gradient(to left, rgb(4,99,17),rgb(22,203,64), #fff,rgb(22,203,64), rgb(4,99,17));"}
color_liner={"w":"linear-gradient(to left,#888,#f5f5f5);",
            "b":"linear-gradient(to left, rgb(0,94,159),#5adcff);",
            "g":"linear-gradient(to left, rgb(4,99,17),rgb(22,203,64));",
            "y":"linear-gradient(to left,#bd9739,#ffd161);",
            "r":"linear-gradient(to left,rgb(212,70,92),rgb(226,85,55));",
            "v":"linear-gradient(to left,rgb(196,44,251),rgb(154,83,249));",
            "side":"linear-gradient(to left,rgb(58, 153, 153),rgb(51,204,204));"
            }


xtMap={"4A":{
        "grid": settings.STATIC_URL+"res/grid4K.svg",
        "1":  [  0, 30,color_liner["y"],200,1.0],
        "2":  [ 30, 30,color_liner["b"],200,1.0],
        "3":  [ 60, 30,color_liner["b"],200,1.0],
        "4":  [ 90, 30,color_liner["y"],200,1.0],
        "A":  [ 0,  60,color_liner["side"],50,0.7],
        "B":  [ 60, 60,color_liner["side"],50,0.7],
        },
        "5A":{
        "grid": settings.STATIC_URL+"res/grid5K.svg",
        "1":  [  0, 24,color_liner["y"],200,1.0],
        "2":  [ 24, 24,color_liner["b"],200,1.0],
        "3":  [ 48, 24,color_liner["y"],200,1.0],
        "4":  [ 72, 24,color_liner["b"],200,1.0],
        "5":  [ 96, 24,color_liner["y"],200,1.0],
        "A":  [ 0,  60,color_liner["side"],50,0.7],
        "B":  [ 60, 60,color_liner["side"],50,0.7],
        },
        "6A":{
        "grid": settings.STATIC_URL+"res/grid6K.svg",
        "1":  [  0, 20,color_liner["y"],200,1.0],
        "2":  [ 20, 20,color_liner["b"],200,1.0],
        "3":  [ 40, 20,color_liner["y"],200,1.0],
        "4":  [ 60, 20,color_liner["y"],200,1.0],
        "5":  [ 80, 20,color_liner["b"],200,1.0],
        "6":  [ 100,20,color_liner["y"],200,1.0],
        "A":  [ 0,  60,color_liner["side"],50,0.7],
        "B":  [ 60, 60,color_liner["side"],50,0.7],
        },
        #8키
        "8A":{#DJMAX
        "grid": settings.STATIC_URL+"res/grid6K.svg",
        "1":  [  0, 20,color_liner["y"],200,1.0],
        "2":  [ 20, 20,color_liner["b"],200,1.0],
        "3":  [ 40, 20,color_liner["y"],200,1.0],
        "4":  [ 60, 20,color_liner["y"],200,1.0],
        "5":  [ 80, 20,color_liner["b"],200,1.0],
        "6":  [ 100,20,color_liner["y"],200,1.0],
        "7":  [  0, 60,color_liner["r"],100,0.9],
        "8":  [ 60, 60,color_liner["r"],100,0.9],
        "A":  [ 0,  60,color_liner["side"],50,0.7],
        "B":  [ 60, 60,color_liner["side"],50,0.7],
        },
        "10A":{#DJMAX
        "grid": settings.STATIC_URL+"res/grid6K.svg",
        "1":  [  0, 20,color_liner["y"],200,1.0],
        "2":  [ 20, 20,color_liner["b"],200,1.0],
        "3":  [ 40, 20,color_liner["y"],200,1.0],
        "4":  [ 60, 20,color_liner["y"],200,1.0],
        "5":  [ 80, 20,color_liner["b"],200,1.0],
        "6":  [ 100,20,color_liner["y"],200,1.0],
        "7":  [  0, 60,color_liner["r"],100,0.9],
        "8":  [ 60, 60,color_liner["r"],100,0.9],
        "9":  [  0, 60,color_liner["v"],70,0.9],
        "0":  [ 60, 60,color_liner["v"],70,0.9],
        "A":  [ 0,  60,color_liner["side"],50,0.7],
        "B":  [ 60, 60,color_liner["side"],50,0.7],
        },
        "SIDE":{#AE23S
        "7":  [  0, 60,color_liner["r"],100,0.9],
        "8":  [ 60, 60,color_liner["r"],100,0.9],
        "A":  [ 0,  60,color_liner["side"],50,0.7],
        "B":  [ 60, 60,color_liner["side"],50,0.7],
        },
    }
#키 순서처리
def keyorder(request,key_val):
    if   key_val==4: key_noran="1234AB"
    elif key_val==5: key_noran="12345AB"
    elif key_val==6: key_noran="123456AB"
    elif key_val==8: key_noran="12345678AB"
    elif key_val==10: key_noran="1234567890AB"

    #미러 구현
    key_mirror = key_noran.replace("AB","").replace("78","").replace("90","")[::-1]
    if key_val==8:
        key_mirror=key_mirror+"87"
    elif key_val==10:
        key_mirror=key_mirror+"8709"
    key_mirror=key_mirror+"BA"

    #랜덤 구현
    key_random= list(key_noran.replace("AB","").replace("78","").replace("90",""))
    key_tri_ran=list("AB")
    random.shuffle(key_random)
    random.shuffle(key_tri_ran)
    key_random=''.join(key_random)
    key_tri_ran=''.join(key_tri_ran)  
    if key_val==8:
        key_random=key_random+key_tri_ran.replace("A","7").replace("B","8")
    elif key_val==10:
        key_random=key_random+key_tri_ran.replace("A","7").replace("B","8")+key_tri_ran.replace("A","9").replace("B","0")
    key_random=key_random+key_tri_ran

    #하프랜덤 구현
    if   key_val==4: 
        key_left="12"
        key_center=""
        key_right="34"
        key_tri="AB"
    elif key_val==5: 
        key_left="12"
        key_center="3"
        key_right="45"
        key_tri="AB"
    elif key_val==6: 
        key_left="123"
        key_center=""
        key_right="456"
        key_tri="AB"
    elif key_val==8: 
        key_left="123"
        key_center=""
        key_right="456"
        key_tri="78AB"
    elif key_val==10: 
        key_left="123"
        key_center=""
        key_right="456"
        key_tri="7890AB"

    key_left= list(key_left)
    key_right= list(key_right)
    random.shuffle(key_left)
    random.shuffle(key_right)
    key_left=''.join(key_left)
    key_right=''.join(key_right)

    key_hrandom=key_left+key_center+key_right+key_tri

    #최종 키순서값
    key_order = request.GET.get('order', key_noran) 

    return key_order, key_mirror, key_random, key_hrandom

#CSS 처리
def innerCSSMake(key_val, key_order, key_type, fx_pattern=False):
    key_char=str(key_val)+key_type
    innerCSS=".bar-note {background-image: url(\""+xtMap[key_char]["grid"]+"\");}\n \
                .note {background: linear-gradient(to left,#888,#f5f5f5); z-index:100;}\n"

    for i in range(key_val):
        innerCSS+=".note-"+str(i)+"{margin-left:"+str(xtMap[key_char][key_order[i]][0])+"px;"+\
                                "width:"+str(xtMap[key_char][key_order[i]][1])+"px;"+\
                                "background:"+xtMap[key_char][key_order[i]][2]+";"+\
                                "z-index:"+str(xtMap[key_char][key_order[i]][3])+";"+\
                                "opacity:"+str(xtMap[key_char][key_order[i]][4])+";}\n"
        
    innerCSS+=".long.note-"+key_order[-2]+"{margin-left:"+str(xtMap["SIDE"]["A"][0])+"px;"+\
                                "width:"+str(xtMap["SIDE"]["A"][1])+"px;"+\
                                "background:"+xtMap["SIDE"]["A"][2]+";"+\
                                "z-index:"+str(xtMap["SIDE"]["A"][3])+";"+\
                                "opacity:"+str(xtMap["SIDE"]["A"][4])+";}\n"
    innerCSS+=".long.note-"+key_order[-1]+"{margin-left:"+str(xtMap["SIDE"]["B"][0])+"px;"+\
                                "width:"+str(xtMap["SIDE"]["B"][1])+"px;"+\
                                "background:"+xtMap["SIDE"]["B"][2]+";"+\
                                "z-index:"+str(xtMap["SIDE"]["B"][3])+";"+\
                                "opacity:"+str(xtMap["SIDE"]["B"][4])+";}\n"
    if fx_pattern:
        innerCSS+=".note-"+key_order[-2].replace("A","6").replace("B","7")+\
                                    "{margin-left:"+str(xtMap["SIDE"]["7"][0])+"px;"+\
                                    "width:"+str(xtMap["SIDE"]["7"][1])+"px;"+\
                                    "background:"+xtMap["SIDE"]["7"][2]+";"+\
                                    "z-index:"+str(xtMap["SIDE"]["7"][3])+";"+\
                                    "opacity:"+str(xtMap["SIDE"]["7"][4])+";}\n"
        innerCSS+=".note-"+key_order[-1].replace("A","6").replace("B","7")+\
                                    "{margin-left:"+str(xtMap["SIDE"]["8"][0])+"px;"+\
                                    "width:"+str(xtMap["SIDE"]["8"][1])+"px;"+\
                                    "background:"+xtMap["SIDE"]["8"][2]+";"+\
                                    "z-index:"+str(xtMap["SIDE"]["8"][3])+";"+\
                                    "opacity:"+str(xtMap["SIDE"]["8"][4])+";}\n"

    return innerCSS

def main_page(request):
    page_info={
        'title': "EZ2PATTERN(DJMAX)",
        'description': "EZ2PATTERN(DJMAX)",
        'canonical_url' : request.build_absolute_uri(request.path),
        'keyword':  "DJMAX",
        'game':"djmax",
        'debug':settings.DEBUG
    }
    context = {
        'page_info': page_info
    }
    return render(request,'djmax/main.html', context)

def index_level(request, keys="4S"):

    # GET 값 받아오기
    page = request.GET.get('page', '1')  
    category = request.GET.get('category', 'ALL') 
    level = request.GET.get('level', 'ALL') 
    sclevel = request.GET.get('sclevel', 'ALL') 
    
    #유효성 검사
    if len(page)>3: raise Http404()
    if len(category)>5: raise Http404()
    if len(level)>4: raise Http404()
    if keys not in ['4B', '5B', '6B', '8B']:       
        raise Http404()

    #DB 불러오기
    song_list = Difficulty.objects.filter(key=keys).order_by('-SC_level', '-MX_level', 'song__name_kr_order')
    
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
    sclevel_int=0
    if level!="ALL":
       song_list = song_list.filter(Q(NM_level=level) | Q(HD_level=level) | Q(MX_level=level)).order_by('song__name_kr_order')
       page_text += "level="+level+"&"
       level_int= int(level)
    if sclevel!="ALL":
       song_list = song_list.filter(Q(SC_level=sclevel)).order_by('song__name_kr_order')
       page_text += "sclevel="+sclevel+"&"
       sclevel_int= int(sclevel)


    #페이지 자르기
    paginator = Paginator(song_list, 40)  
    page_obj = paginator.get_page(page)
    num_page = paginator.num_pages
      
    #페이지 제목
    if "B" in keys:
        title_sub = keys.replace('B',' ')+"BUTTON"
    page_info={
        'title': "EZ2PATTERN(DJMAX) - "+ title_sub,
        'description': "EZ2PATTERN(DJMAX) - "+ title_sub,
        'canonical_url' : request.build_absolute_uri(request.path),
        'keyword':  "DJMAX",
        'game':"djmax",
        'debug':settings.DEBUG
    }
    context = {
        'page_info': page_info,

        'song_list': page_obj,
        
        'key':keys,
        'page_text':page_text,
        'num_page':num_page,
        'level':level_int,
        'sclevel':sclevel_int,
    }
    return render(request,'djmax/index_level.html',context)



def detail_chart(request, page_name, song_id=0, keys="XB", difficulty="MX"):
    if song_id != 0:
        song = get_object_or_404(Song, pk=song_id)
    else:
        song = get_object_or_404(Song, page_name=page_name)
        song_id = song.id

    #DB에서 패턴 데이터 불러오기
    pattern_data = None  
    try:
        pattern_data = song.pattern_set.get(key=keys, difficulty=difficulty)  
    except ObjectDoesNotExist:
        pattern_data = None  

    # 패턴 파일 읽어오기
    file_name="./chart/djmax/"
    file_name+= str(song_id)+"/"+difficulty+"."+keys
    with open(file_name+".html", "r", encoding='utf8') as p:
        innerHTML = p.read()

    #키순서 처리
    if keys=="XB":
        key_val=10
    else:
        key_val=int(keys.replace("B","").replace("S","").replace("X","").replace("K",""))
    (key_order, key_mirror, key_random, key_hrandom)=keyorder(request,key_val)
    if len(key_order)!=key_val+2: raise Http404()
    
    
    if len(difficulty)>10: raise Http404()

    #CSS 처리
    if difficulty=="FX":
        fx_pattern=True
    else:  
        fx_pattern=False
    key_type = request.GET.get('type', "A") 
    innerCSS=innerCSSMake(key_val,key_order,key_type,fx_pattern)

    page_info={
        'title': "EZ2PATTERN(DJMAX) - " + song.name_kr + " " + keys + " " + difficulty,
        'description': "EZ2PATTERN(DJMAX) - " + song.name_kr + " " + keys + " " + difficulty,
        'canonical_url' : request.build_absolute_uri(request.path),
        'keyword':  "DJMAX",
        'game':"djmax",
        'debug':settings.DEBUG
    }

    context={
        'page_info': page_info,

        'key_mirror':key_mirror,
        'key_random':key_random,
        'key_hrandom':key_hrandom,
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
    return render(request, 'djmax/detail_chart.html', context)

