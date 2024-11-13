from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Task, Description
from .forms import TaskForm
from .forms import CreateForm
from django.forms.fields import CharField
import json
from openai import OpenAI
from .calendarapi import GoogleCalendarHelper

def calendarTask(request, pk):
    SingleTask = Task.objects.get(id=pk)

    print('SingleTask:', SingleTask)
    return render(request, 'tasks/single-task.html', {'project': SingleTask})


#def home(request):x    
    #return HttpResponse('Homepage')

def allTasks(request):
    tasks = Task.objects.all()
    context={'Tasks':tasks}
    return render(request, 'tasks/alltasks.html', {'tasks': tasks})

def EditTask(request):
    edit = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            CalendarUpdate()
            return redirect('alltasks')

    #context = {'edit': edit}
    return render(request, 'tasks/edit_form.html', {'edit': edit})

def UpdateTask(request, pk):
    task = Task.objects.get(id=pk)
    edit = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            CalendarUpdate()
            return redirect('alltasks')
    context = {'edit': edit}
    #context = {'edit': edit}   
    return render(request, 'tasks/edit_form.html', context)

def CalendarUpdate():
    print(Task.objects.all().order_by('due_date','importance'))
    helper = GoogleCalendarHelper()
    helper.delete_events()
    for task in Task.objects.all().order_by('due_date','importance'):
        helper.create_event(task)
        



def DeleteTask(request, pk):
    task = Task.objects.get(id=pk)

    if request.method == 'POST':
        task.delete()
        CalendarUpdate()
        return redirect('alltasks')
    delete = TaskForm(instance=task)
    return render(request, 'tasks/delete_object.html', {'delete': delete} )

def CreateTask(request):
    form = CreateForm(request.POST, request.FILES)
    if form.is_valid():
        task = task_from_description(form.cleaned_data['description'])
        
        task.save()
        return redirect(f"/update_task/{task.id}/")
    
    context = {'form': form}
    return render(request, "tasks/create_form.html", context)   

def task_from_description(description):
    client = OpenAI(api_key='')
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"Provide your response as a JSON object that represents a calendar entry for a school task given USER_TEXT with the following schema:\n{{\n    \"title\":  \"\",\n    \"description\":  \"\",\n     \"importance\": \"low, medium or high\",\n     \"due_date\": date_time,\n     \"subject\": \"class subject\"\n}}\n\nUSER_TEXT:\n{description}"
                }
            ]
            }
        ],
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )
    task_json = json.loads(response.choices[0].message.content)
    task = Task()
    if 'title' in task_json:
        task.title = task_json['title']
    else:
        task.title = ''
    
    if 'description' in task_json:
        task.description = task_json['description']
    else:
        task.description = ''

    if 'importance' in task_json:
        if 'importance' == 'high':
            task.importance = 3
        elif 'importance' == 'medium':
            task.importance = 2
        elif 'importance' == 'low':
            task.importance == 1
        else:
            task.importance = 2
    else:
        task.importance = 2

    if 'due_date' in task_json:
        task.due_date = task_json['due_date']
    else:
        task.due_date = ''    

    if 'subject' in task_json:
        task.subject = task_json['subject']
    else:
        task.subject = ''



    return task
    