from django.db import models
import uuid

class Description(models.Model):
    description = models.TextField(null=True, blank = False)



class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default='default.jpg')
    importance = models.IntegerField(null=False)
    due_date = models.CharField(max_length=200, null=False)
    subject = models.CharField(max_length=200, null=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    duration = models.IntegerField(default=1, null=False)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    vote_type = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
        )
    #owner =
    project = models.ForeignKey(Task, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=vote_type)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
    