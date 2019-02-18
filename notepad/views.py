from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteModelForm

# Create your views here.

def create_view(request):
    
    form = NoteModelForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect('/')

    context = {
        'form': form,
    }

    return render(request, "notepad/create.html", context)

def list_view(request):
    notes = Note.objects.all()

    context = {
        'object_list': notes
    }

    return render(request, 'notepad/list.html', context)

def delete_view(request, id):
    note_to_delete = Note.objects.filter(pk=id) #returns a list. grab first and only item
    if note_to_delete.exists():
        if request.user == note_to_delete[0].user:
            note_to_delete[0].delete()
    return redirect('/')

def update_view(request, id):
    note_to_update = get_object_or_404(Note, id=id)
    form = NoteModelForm(request.POST or None, request.FILES or None, instance=note_to_update)

    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect('/')

    context = {
        'form': form,
    }

    return render(request, "notepad/create.html", context)