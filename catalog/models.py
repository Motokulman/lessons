from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # Required for unique instances

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a video genre')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Language(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a language')
    
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






class CourseType(models.Model):
    name = models.TextField(max_length=100)
    ancestor_type = models.TextField(max_length=100)
    image = models.ImageField(max_length=100, help_text='Upload preview for this CourseType')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name
        
class Video(models.Model):
    """Model representing a entertaining video (not a lesson video)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular video')
    title = models.CharField(max_length=200)
    producer = models.ManyToManyField(Producer, help_text='Select a producer of this video')
    description = models.TextField(max_length=1000, help_text='Enter a description of the video')
    # ManyToManyField used because genre can contain many vids. Vids can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this video')
    duration = models.TimeField(max_length=13) # Make it autoset
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    technology = models.ForeignKey('Technology', on_delete=models.SET_NULL, null=True, help_text='Select a related technology: computer animation, drawed, e.t.c.')
    image = models.ImageField(max_length=100, help_text='Upload preview for video')
    serial = models.ForeignKey('Serial', on_delete=models.SET_NULL, null=True, help_text='Select a related serial for this video')
    logia = models.ForeignKey('Logia', on_delete=models.SET_NULL, null=True, help_text='Select a related logia for this video')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access this video."""
        return reverse('video-link', args=[str(self.id)])

class Producer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular producer')
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, help_text='Enter a description of the producer')

    ROLE = (
        ('e', 'Entertaining video'),
        ('l', 'Lessons'),
        ('b', 'Both'),
    )
        
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular course')
    title = models.CharField(max_length=200)
    producer = models.ManyToManyField(Producer, help_text='Select a producer of this course')
    course_type = models.ForeignKey(CourseType, on_delete=models.SET_NULL, null=True, help_text="It's quite enough to store only last course type cause all the chain can be restored automatically")
    description = models.TextField(max_length=1000, help_text='Enter a description for this course')
    common_age_from = models.TimeField()
    common_age_to = models.TimeField()
    recommended_age_from = models.TimeField()
    recommended_age_to = models.TimeField()
    algorithm = models.ForeignKey('Algorithm', on_delete=models.SET_NULL, null=True, help_text="Algorithm for pithing this course")
    image = models.ImageField(max_length=100, help_text='Upload preview for this course')
    

    def __str__(self):
        """String for representing the Model object."""
        return self.title



class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular video')
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, help_text='Enter a description of the video')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    duration = models.TimeField(max_length=13) # Make it autoset
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, help_text='Select course of this lesson')
    order = models.IntegerField(help_text='Order this lesson during course')
    image = models.ImageField(max_length=100, help_text='Upload preview for this lesson')
    varles_1 = models.CharField(max_length=50, help_text='Reserved var for set up the algorithm.')
    varles_2 = models.CharField(max_length=50, help_text='Reserved var for set up the algorithm.')
    varles_3 = models.CharField(max_length=50, help_text='Reserved var for set up the algorithm.')
    
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
    user =  models.ForeignKey(help_text="Which user have this child")
    name = models.CharField(max_length=200, help_text="Name of this child")
    date_of_birth = models.DateField(null=True, blank=True)  
    completed_courses = models.ManyToManyField()
    current_lessons = models.ManyToManyField() # Theorethically possible to study some courses simultaneously. Quite enough to store only current lesson cause course can be defined automatically
    planned_courses = models.ManyToManyField()
    image = models.ImageField(max_length=100, help_text='Upload avatar for this pupil')
    
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