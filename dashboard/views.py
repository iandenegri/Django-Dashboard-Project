import math
from datetime import timedelta, timezone, datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from notepad.forms import NoteModelForm
from notepad.models import Note

from news.models import Headline, UserProfile


@login_required
def home(request):
    user_profile = UserProfile.objects.filter(user=request.user).first()
    now = datetime.now(timezone.utc)

    if user_profile.last_scrape_time:
        time_difference = now - user_profile.last_scrape_time
        # Convert time difference to minutes to check if it's been an hour
        time_difference_in_minutes = time_difference/timedelta(seconds=60)
        next_scrape = (60 - time_difference_in_minutes)

        if time_difference_in_minutes <= 60:
            # Bring up message to not scrape
            deny_permission = True
        else:
            deny_permission = False
    else:
        next_scrape = 0
        deny_permission = False

    headlines = Headline.objects.all()
    notes = Note.objects.filter(user=request.user)

    form = NoteModelForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect('/')

    context = {
        "form": form,
        "notes_list": notes,
        "object_list": headlines,
        "deny_permission": deny_permission,
        "next_scrape": math.ceil(next_scrape)
    }
    
    return render(request, 'news/home.html', context=context)