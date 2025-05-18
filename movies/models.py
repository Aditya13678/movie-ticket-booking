from django.db import models

# Create your models here.

genres=[
    ['action','Action'],
    ['comedy','Comedy'],
    ['drama','Drama'], 
    ['horror','Horror'],
    ['romance','Romance'],
    ['thriller','Thriller'],
    ['sci-fi','Sci-Fi'],
    ['fantasy','Fantasy'],
    ['animation','Animation'],
    ['documentary','Documentary'],
    ['crime','Crime'],
    ['adventure','Adventure'],
    ['mystery','Mystery'],
    ['family','Family'],
    ['musical','Musical'],
    ['western','Western'], 
]

languages=[
    ['english','English'],
    ['spanish','Spanish'],
    ['tamil','Tamil'],
    ['kannada','Kannada'],
    ['telugu','Telugu'],
    ['hindi','Hindi'],
    ['french','French'],
    ['german','German'],
    ['chinese','Chinese'],
    ['japanese','Japanese'],
    ['korean','Korean'],
    ['portuguese','Portuguese'],
    ['arabic','Arabic'],
    ['russian','Russian'],
    ['italian','Italian'],
    ['dutch','Dutch'],
]

class Movie(models.Model):
    movie_id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    genre=models.CharField(max_length=255,choices=genres)
    language=models.CharField(max_length=255,choices=languages)
    synopsis=models.TextField()
    cast=models.TextField()
    duration_minutes=models.IntegerField()
    release_date=models.DateField()
    thriller_url=models.CharField(max_length=2000,null=True,blank=True)
    status=models.CharField(max_length=255,null=True,blank=True)
    image=models.CharField(max_length=4000,null=True,blank=True)

    slug=models.CharField(max_length=2000,null=True,blank=True)

    def save(self,*args,**kwargs):
        self.slug=self.title.replace(' ','-')
        super().save(*args,*kwargs)


    def __str__(self):
        return self.title




class search_movies_by_name(models.Model):
    moviename=models.CharField(max_length=2000)
    
