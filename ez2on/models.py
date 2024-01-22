from django.db import models

# Create your models here.
class Song(models.Model):
    DEFAULT_CATEGORY = "ALL"
    CATEGORY_CHOICES = [
        (DEFAULT_CATEGORY, "No category"),
        ("1ST", "1ST TRACKS"),
        ("SE", "SPECIAL EDITION"),
        ("2ND", "2nd TRAX"),
        ("3RD", "3rd TRAX"),
        ("4TH", "4th TRAX"),
        ("PT", "PLATINUM"),
        ("6TH", "6th TRAX"),
        ("7TH", "7th TRAX"),
        ("2008", "2008 (RETRO)"),
        ("2013", "2013 (REBOOT)"),
        ("2021", "2021 (REBOOT:R)"),
        ("TT", "TIME TRAVELER"),
        ("CV", "CODENAME VIOLET"),
        ("PP", "PRESTIGE PASS"),
        ("O2", "O2JAM COLLAB"),
        ("GC", "GROOVE COASTER COLLAB"),
        ("EC", "ENDLESS CIRCULATION"),
        ("FT", "FORTRESS COLLAB"),
        ("DM", "DJMAX COLLAB"),
    ]
    name_kr       = models.CharField(max_length=100)
    name_kr_order  = models.IntegerField(default=0)
    page_name  = models.CharField(max_length=100,unique=True)
    composer   = models.CharField(max_length=100)
    # visualizer = models.CharField(max_length=100, blank=True)
    genre      = models.CharField(max_length=100, blank=True)
    category   = models.CharField(max_length=10,choices=CATEGORY_CHOICES, default=DEFAULT_CATEGORY)

    # bpm      = models.FloatField(default=0) # don't use this
    min_bpm      = models.FloatField(default=0)
    max_bpm      = models.FloatField(default=0)

    playtime = models.CharField(max_length=10)
    update_date = models.DateField(auto_now_add=False)
    deleted = models.BooleanField(default = False)
    
    def __str__(self):
        return self.name_kr

class Difficulty(models.Model):
    DEFAULT_KEY="NA"
    KEY_CHOICES = [
        (DEFAULT_KEY, "Not Value"),
        ("4S", "4K Standard"),
        ("5S", "5K Standard"),
        ("6S", "6K Standard"),
        ("8S", "8K Standard"),
        ("4B", "4K Basic"),
        ("5B", "5K Basic"),
        ("6B", "6K Basic"),
        ("8B", "8K Basic"),
    ]
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    key = models.CharField(max_length=2,choices=KEY_CHOICES, default=DEFAULT_KEY)

    EZmix_level  = models.IntegerField(default=0)
    NMmix_level  = models.IntegerField(default=0)
    HDmix_level  = models.IntegerField(default=0)
    SHDmix_level = models.IntegerField(default=0)
    # EZmix_note        = models.IntegerField(default=0)
    # NMmix_note        = models.IntegerField(default=0)
    # HDmix_note        = models.IntegerField(default=0)
    # SHDmix_note       = models.IntegerField(default=0)
    EZmix_pattern     = models.BooleanField(default = False)
    NMmix_pattern     = models.BooleanField(default = False)
    HDmix_pattern     = models.BooleanField(default = False)
    SHDmix_pattern    = models.BooleanField(default = False)
    def __str__(self):
        return str(self.song.name_kr)+'|'+str(self.key)


class Course(models.Model):
    DEFAULT_KEY=0
    KEY_CHOICES = [
        (DEFAULT_KEY, "Not Value"),
        ("4K", "4K Standard"),
        ("5K", "5K Standard"),
        ("6K", "6K Standard"),
        ("8K", "8K Standard"),
        ("SP", "SPECIAL"),
    ]
    DEFAULT_DLC = "NA"
    DLC_CHOICES = [
        (DEFAULT_DLC, "No DLC"),
        ("TT", "TIME TRAVELER"),
        ("CV", "CODENAME VIOLET"),
        ("PP", "PRESTIGE PASS"),
        ("O2", "O2JAM COLLAB"),
        ("GC", "GROOVE COASTER COLLAB"),
        ("EC", "ENDLESS CIRCULATION"),
        ("FT", "FORTRESS COLLAB"),
        ("DM", "DJMAX COLLAB"),
    ]
    #song = models.ForeignKey(Song, on_delete=models.CASCADE)
    key           = models.CharField(max_length=2,choices=KEY_CHOICES, default=DEFAULT_KEY)
    name_kr       = models.CharField(max_length=100)
    page_name     = models.CharField(max_length=100,unique=True)
    # subname_kr    = models.CharField(max_length=200)
    level         = models.CharField(max_length=10)
    level_int     = models.IntegerField(default=0)
    patterner     = models.CharField(max_length=100)

    song_key1         = models.CharField(max_length=10)
    song_key2         = models.CharField(max_length=10)
    song_key3         = models.CharField(max_length=10)
    song_key4         = models.CharField(max_length=10)
    
    ingame_order  = models.IntegerField(default=0)
    ac_chal = models.BooleanField(default = False)
    cc_chal = models.BooleanField(default = False)
    update_date = models.DateField(auto_now_add=False)
    deleted = models.BooleanField(default = False)
    file_name              =models.TextField(max_length=20, null=True)
    show_pattern    = models.BooleanField(default = False)

    song1             = models.ForeignKey(Song, related_name='corse1_set', on_delete=models.SET_NULL, null=True)
    song2             = models.ForeignKey(Song, related_name='corse2_set', on_delete=models.SET_NULL, null=True)
    song3             = models.ForeignKey(Song, related_name='corse3_set', on_delete=models.SET_NULL, null=True)
    song4             = models.ForeignKey(Song, related_name='corse4_set', on_delete=models.SET_NULL, null=True)
    

    def __str__(self):
        return str(self.key)+'|'+str(self.name_kr)

  
class Pattern(models.Model):
    DEFAULT_KEY="NA"
    KEY_CHOICES = [
        (DEFAULT_KEY, "Not Value"),
        ("4S", "4K Standard"),
        ("5S", "5K Standard"),
        ("6S", "6K Standard"),
        ("8S", "8K Standard"),
        ("4B", "4K Basic"),
        ("5B", "5K Basic"),
        ("6B", "6K Basic"),
        ("8B", "8K Basic"),
        ("CO", "Course"),
    ]
    key = models.CharField(max_length=2,choices=KEY_CHOICES, default=DEFAULT_KEY)
    level = models.IntegerField(default=0) 
    sublevel = models.CharField(max_length=10,default=0) 
    difficulty = models.CharField(max_length=40)
    notes        = models.IntegerField(default=0)

    notes_groove        = models.IntegerField(default=0)
    climax_groove        = models.IntegerField(default=0)
    multi_groove        = models.IntegerField(default=0)
    long_groove       = models.IntegerField(default=0)
    mayhem_groove       = models.IntegerField(default=0)

    show_pattern   = models.BooleanField(default = False)

    def __str__(self):
        return self.song.name_kr+"|"+self.key+" "+self.difficulty

    song = models.ForeignKey(Song, on_delete=models.CASCADE)

# class CourseComponent (models.Model):
#     song             = models.ForeignKey(Song,on_delete=models.SET_NULL,null=True)
#     course           = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    
#     song_index       = models.IntegerField(default=1) #몇번째 곡?
#     song_key         = models.CharField(max_length=10)
#     song_note        = models.IntegerField(default=0)

#     def __str__(self):
#         return str(self.course.key)+'|'+str(self.course.name_kr)+'|'+str(self.song.name_kr)