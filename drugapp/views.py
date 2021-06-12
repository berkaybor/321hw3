from django.shortcuts import render
from .database import edit_reaction_affinity
from .forms import ReactionAffinityEditForm

def home(request):
    return render(request, 'drugapp/home.html')

def update_reaction_affinity(request):
    if request.method == 'GET':
        context = {'form': ReactionAffinityEditForm()}
        return render(request, 'drugapp/update_reaction_affinity.html', context)
    elif request.method == 'POST':
        form = ReactionAffinityEditForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            msg = edit_reaction_affinity(f['reaction_id'], f['affinity'])

        if msg:
            return render(request, 'drugapp/update_reaction_affinity.html', {'msg': msg, 'form': ReactionAffinityEditForm()})  

        return render(request, 'users/add_user.html', {'msg': 'Reaction afiinity modified', 'form': ReactionAffinityEditForm()})