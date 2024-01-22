from django.db import models

# Create your models here.
class Song(models.Model):
    name_kr       = models.CharField(max_length=100)
    name_kr_order  = models.IntegerField(default=0)
    page_name  = models.CharField(max_length=100,unique=True)
    composer   = models.CharField(max_length=100)
    category   = models.CharField(max_length=10,default="ALL")

    min_bpm      = models.FloatField(default=0)
    max_bpm      = models.FloatField(default=0)

    update_date = models.DateField(auto_now_add=False)
    deleted = models.BooleanField(default = False)
    
    def __str__(self):
        return self.name_kr

class Difficulty(models.Model):
    DEFAULT_KEY="NA"
    KEY_CHOICES = [
        (DEFAULT_KEY, "Not Value"),
        ("4B", "4BUTTON"),
        ("5B", "5BUTTON"),
        ("6B", "6BUTTON"),
        ("8B", "8BUTTON"),
    ]
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    key = models.CharField(max_length=2,choices=KEY_CHOICES, default=DEFAULT_KEY)

    NM_level  = models.IntegerField(default=0)
    HD_level  = models.IntegerField(default=0)
    MX_level  = models.IntegerField(default=0)
    SC_level  = models.IntegerField(default=0)
    NM_pattern = models.BooleanField(default = False)
    HD_pattern = models.BooleanField(default = False)
    MX_pattern = models.BooleanField(default = False)
    SC_pattern = models.BooleanField(default = False)
    def __str__(self):
        return str(self.song.name_kr)+'|'+str(self.key)
    
class Pattern(models.Model):
    DEFAULT_KEY="NA"
    KEY_CHOICES = [
        (DEFAULT_KEY, "Not Value"),
        ("4B", "4BUTTON"),
        ("5B", "5BUTTON"),
        ("6B", "6BUTTON"),
        ("8B", "8BUTTON"),
    ]
    key = models.CharField(max_length=2,choices=KEY_CHOICES, default=DEFAULT_KEY)
    level = models.IntegerField(default=0) 
    floor = models.FloatField(default=0) 
    difficulty = models.CharField(max_length=40)
    notes        = models.IntegerField(default=0)

    # notes_groove        = models.IntegerField(default=0)
    # climax_groove        = models.IntegerField(default=0)
    # multi_groove        = models.IntegerField(default=0)
    # long_groove       = models.IntegerField(default=0)
    # mayhem_groove       = models.IntegerField(default=0)

    pattern_maker = models.CharField(max_length=40)
    show_pattern   = models.BooleanField(default = False)

    def __str__(self):
        return self.song.name_kr+"|"+self.key+" "+self.difficulty

    song = models.ForeignKey(Song, on_delete=models.CASCADE)