from django.forms import ModelForm
from .models import Task, Description


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'


class CreateForm(ModelForm):
    class Meta:
        model = Description
        fields = '__all__'









