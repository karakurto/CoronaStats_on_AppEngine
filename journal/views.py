from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

import os.path
from os import path

from .cantonal_rankings import rankings
from datetime import datetime, timedelta

def index(request):
    """The home page for Learning Log."""
    return render(request, 'journal/index.html')

def public_topics(request):
    """Show all public topics."""
    topics = Topic.objects.filter(owner=3).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'journal/public_topics.html', context)

def public_topic(request, topic_id):
    """Show a single public topic and all its entries."""
    topic = Topic.objects.get(id=topic_id, owner=3)
    # Make sure the topic belongs to the current user.

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'journal/public_topic.html', context)

def corona_stats_ch(request):
    yesterday_raw = datetime.now() - timedelta(days=1)
    yesterday = yesterday_raw.strftime("%Y-%m-%d")
    corona_stats_ch_loc = f'/tmp/corona_stats_{yesterday}.html'
    if path.exists(corona_stats_ch_loc):
        return render(request, corona_stats_ch_loc)
    else:
        rankings()
        if path.exists(corona_stats_ch_loc):
            return render(request, corona_stats_ch_loc)
        else:
            return render(request, 'journal/corona_stats_not_exist.html')
    
@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'journal/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'journal/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('journal:topics')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'journal/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
        
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('journal:topic', topic_id=topic_id)

    # Display a blank or invalid form.
    context = { 'topic': topic, 'form': form}
    return render(request, 'journal/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit and existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initail request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted, process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('journal:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'journal/edit_entry.html', context)