from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # Required for unique instances
from mptt.models import MPTTModel, TreeForeignKey # for hierarchical data
from django.contrib.auth.models import User

class Genre(models.Model):
    """Model representing a video genre."""
    name = models.CharField(max_length=200, help_text='Enter a video genre')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Country(models.Model):
    """Model representing a country"""
    name = models.CharField(max_length=200, help_text='Enter a country')
        
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Language(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a language')
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, help_text="Related country for this language")
   
    LANGUAGE_STATUS = (
        ('o', 'Official language'),
        ('r', 'Regional language'),
    )
            
    status = models.CharField(
        max_length=1,
        choices=LANGUAGE_STATUS,
        blank=True,
        default='o',
        help_text="Is this language official for this country or it regional",
    )
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name



class Serial(models.Model):
    name = models.CharField(max_length=200, help_text="Name of this serial")
    description = models.TextField(max_length=1000, help_text='Enter a description for this serial')
        
    def __str__(self):
        """String for representing the Model object."""
        return self.name    

class Logia(models.Model):
    name = models.CharField(max_length=200, help_text="Name of this logia. The videos for the same story but different producers")
    description = models.TextField(max_length=1000, help_text='Enter a description for this logia')
        
    def __str__(self):
        """String for representing the Model object."""
        return self.name    


class Technology(models.Model):
    name = models.CharField(max_length=200, help_text="Name of technology: computer animation, drawed, e.t.c.")
    description = models.TextField(max_length=1000, help_text='Enter a description for this technology')
        
    def __str__(self):
        """String for representing the Model object."""
        return self.name    

class Producer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular producer')
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, help_text='Enter a description of the producer')

    ROLE = (
        ('e', 'Entertaining video'),
        ('l', 'Lessons'),
        ('b', 'Both'),
    )
            
    status = models.CharField(
        max_length=1,
        choices=ROLE,
        blank=True,
        default='e',
        help_text="Do you produce entertaining video, lessons video or both",
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class CourseType(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(max_length=100, null=True, help_text='Upload preview for this CourseType')


    class MPTTMeta:
        order_insertion_by = ['name']

    #def __str__(self):
        """String for representing the Model object."""
       # return self.name


        
class Video(models.Model):
    """Model representing a entertaining video (not a lesson video)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular video')
    title = models.CharField(max_length=200)
    path = models.URLField(max_length=200, blank=True, help_text='Set url path for this video')
    producer = models.ManyToManyField(Producer, blank=True, help_text='Select a producer of this video')
    description = models.TextField(max_length=1000, null=True, blank=True, help_text='Enter a description of the video')
    # ManyToManyField used because genre can contain many vids. Vids can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, blank=True, help_text='Select a genre for this video')
    duration = models.TimeField(max_length=13, null=True, blank=True) # Make it autoset
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    technology = models.ForeignKey('Technology', on_delete=models.SET_NULL, null=True, blank=True, help_text='Select a related technology: computer animation, drawed, e.t.c.')
    image = models.ImageField(max_length=100, null=True, blank=True, help_text='Upload preview for video')
    serial = models.ForeignKey('Serial', on_delete=models.SET_NULL, null=True, blank=True, help_text='Select a related serial for this video')
    logia = models.ForeignKey('Logia', on_delete=models.SET_NULL, null=True, blank=True, help_text='Select a related logia for this video')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access this video."""
        return reverse('video-link', args=[str(self.id)])



class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular course')
    title = models.CharField(max_length=200)
    producer = models.ManyToManyField(Producer, blank=True, help_text='Select a producer of this course')
    course_type = models.ForeignKey(CourseType, on_delete=models.SET_NULL, null=True, blank=True,  help_text="It's quite enough to store only last course type cause all the chain can be restored automatically")
    description = models.TextField(max_length=1000, null=True, blank=True, help_text='Enter a description for this course')
    common_age_from = models.IntegerField(null=True, blank=True)
    common_age_to = models.IntegerField(null=True, blank=True)
    recommended_age_from = models.IntegerField(null=True, blank=True)
    recommended_age_to = models.IntegerField(null=True, blank=True)
    algorithm = models.ForeignKey('Algorithm', on_delete=models.SET_NULL, null=True, blank=True, help_text="Algorithm for pithing this course")
    image = models.ImageField(max_length=100, null=True, blank=True, help_text='Upload preview for this course')
    teaching_language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, blank=True, related_name='teaching_language', help_text='Select a language of teaching')
    is_language = models.BooleanField(default=False, null=True, blank=True, help_text='Is this course for study language?')
    target_language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, blank=True, related_name='target_language', help_text='Select a target language, if this is language course')
 
    def __str__(self):
        """String for representing the Model object."""
        return self.title



class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular lesson')
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True, help_text='Select course of this lesson')
    title = models.CharField(max_length=200)
    path = models.URLField(max_length=200, blank=True, help_text='Set url path for this lesson')
    description = models.TextField(max_length=1000, null=True, blank=True, help_text='Enter a description of the video')
    duration = models.TimeField(max_length=13, null=True, blank=True, ) # Make it autoset
    order = models.IntegerField(null=True, blank=True, help_text='Order this lesson during course')
    image = models.ImageField(max_length=100, null=True, blank=True, help_text='Upload preview for this lesson')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access this lesson."""
        return reverse('lesson-link', args=[str(self.id)])


class Algorithm(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=1000, help_text='Enter a description for this Algorithm')
    # Set up how many times specified lesson with defined mark must be repeated
        
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Pupil(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # whose this pupil
    name = models.CharField(max_length=200, help_text="Name of this child")
    date_of_birth = models.DateField(null=True, blank=True)  
    completed_courses = models.ManyToManyField(Course, blank=True, related_name='completed_courses')
    current_lessons = models.ManyToManyField(Lesson, blank=True) # Theorethically possible to study some courses simultaneously. Quite enough to store only current lesson cause course can be defined automatically
    planned_courses = models.ManyToManyField(Course, blank=True, related_name='planned_courses')
    image = models.ImageField(max_length=100, null=True, blank=True, help_text='Upload avatar for this pupil')
    native_language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True, help_text="Your country uses for defining official and regional languages in your location")
    
    GENDER = (
        ('b', 'Boy'),
        ('g', 'Girl'),
    )
    
    status = models.CharField(
        max_length=1,
        choices=GENDER,
        blank=True,
        default='b',
        help_text="Choose pupil's gender",
    )
        
    def __str__(self):
        """String for representing the Model object."""
        return self.name    
