from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

@login_required # this decorator ensures that the user is logged in before they can access this view
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added') # the filter() method returns a queryset containing the requested data
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added') # the minus sign sorts in reverse order
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST': # No data submitted; create a blank form.
        form = TopicForm()
    else: # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user # Assign owner here
            new_topic.save()
            return redirect('learning_logs:topics')
            """form.save()
            return redirect('learning_logs:topics') # redirect the user to the topics page"""
    
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST': # No data submitted; create a blank form.
        form = EntryForm()
    else: # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False) # save the form to a new object without saving it to the database
            new_entry.topic = topic # set the topic of the new entry to the topic we pulled from the database
            new_entry.save() # save the new entry to the database
            return redirect('learning_logs:topic', topic_id=topic_id) # redirect the user to the topic page
    
    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id) # get the entry object from the database
    topic = entry.topic # get the topic of the entry
    
    if request.method != 'POST': # No data submitted; create a blank form.
        form = EntryForm(instance=entry) # create a form instance that is pre-filled with information from the entry object
    else: # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST) # create a form instance that is pre-filled with information from the entry object and the submitted data
        if form.is_valid():
            form.save() # save the form to the entry object
            return redirect('learning_logs:topic', topic_id=topic.id) # redirect the user to the topic page
    
    # Display a blank or invalid form.
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)