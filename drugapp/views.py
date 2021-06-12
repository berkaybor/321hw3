from django.shortcuts import render
from .forms import *
from .database import *


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

        return render(request, 'drugapp/update_reaction_affinity.html', {'msg': 'Reaction afinity modified', 'form': ReactionAffinityEditForm()})


def delete_drug(request):
    if request.method == 'GET':
        context = {'form': GetDrugForm()}
        return render(request, 'drugapp/delete_drug.html', context)
    elif request.method == 'POST':
        form = GetDrugForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            msg = delete_drug_from_db(f['drug_id'])

        if msg:
            return render(request, 'drugapp/delete_drug.html', {'msg': msg, 'form': GetDrugForm()})

        return render(request, 'drugapp/delete_drug.html', {'msg': 'Drug deleted', 'form': GetDrugForm()})


def delete_protein(request):
    if request.method == 'GET':
        context = {'form': GetProtein()}
        return render(request, 'drugapp/delete_protein.html', context)
    elif request.method == 'POST':
        form = GetProtein(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            msg = delete_prot_from_db(f['uniprot_id'])
            if msg:
                return render(request, 'drugapp/delete_protein.html', {'msg': msg, 'form': GetProtein()})
        else:
            return render(request, 'drugapp/delete_protein.html', {'msg': 'Wrong input', 'form': GetProtein()})

        return render(request, 'drugapp/delete_protein.html', {'msg': 'Protein deleted', 'form': GetProtein()})


def drug_interactions(request):
    if request.method == 'GET':
        context = {'form': GetDrugForm()}
        return render(request, 'drugapp/view_all_interactions.html', context)
    elif request.method == 'POST':
        form = GetDrugForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            interacted_drugs = drug_interactions_db(f['drug_id'])
            if not interacted_drugs:
                return render(request, 'drugapp/view_all_interactions.html', {'msg': 'Drug not found', 'form': GetDrugForm()})
        else:
            return render(request, 'drugapp/view_all_interactions.html', {'msg': 'Wrong input', 'form': GetDrugForm()})

        interacted_drugs = [i[0] for i in interacted_drugs]
        return render(request, 'drugapp/view_all_interactions.html', {'form': GetDrugForm(), 'drugs': interacted_drugs})


def view_side_effects(request):
    if request.method == 'GET':
        context = {'form': GetDrugForm()}
        return render(request, 'drugapp/side_effects.html', context)
    elif request.method == 'POST':
        form = GetDrugForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            side_effects = view_side_effects_db(f['drug_id'])
            if not side_effects:
                return render(request, 'drugapp/side_effects.html', {'msg': 'Drug not found', 'form': GetDrugForm()})
        else:
            return render(request, 'drugapp/side_effects.html', {'msg': 'Wrong input', 'form': GetDrugForm()})

        side_effects = [{'umls_cui': s[0], 'name': s[1]} for s in side_effects]
        return render(request, 'drugapp/side_effects.html', {'form': GetDrugForm(), 'side_effects': side_effects})


def view_interacting_targets(request):
    if request.method == 'GET':
        context = {'form': GetDrugForm()}
        return render(request, 'drugapp/interacting_targets.html', context)
    elif request.method == 'POST':
        form = GetDrugForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            interacting_targets = view_interacting_targets_db(f['drug_id'])
            if not interacting_targets:
                return render(request, 'drugapp/interacting_targets.html', {'msg': 'Drug not found', 'form': GetDrugForm()})
        else:
            return render(request, 'drugapp/interacting_targets.html', {'msg': 'Wrong input', 'form': GetDrugForm()})

        interacting_targets = [{'uniprot_id': t[0], 'name': t[1]} for t in interacting_targets]
        return render(request, 'drugapp/interacting_targets.html', {'form': GetDrugForm(), 'interacting_targets': interacting_targets})


def listDrugs(request):
    drugs = return_drugs()
    drugs_dict = {"drugs_list": drugs}
    return render(request, 'drugapp/home.html', drugs_dict)


def showDrug(request, drugid):
    anan = return_drug_details(drugid)
    drug_dict = {"drug_details": anan}
    return render(request, 'drugapp/drug_detail.html', anan)
