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
            return render(request, 'drugapp/update_reaction_affinity.html',
                          {'msg': msg, 'form': ReactionAffinityEditForm()})

        return render(request, 'drugapp/update_reaction_affinity.html',
                      {'msg': 'Reaction afinity modified', 'form': ReactionAffinityEditForm()})


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
                return render(request, 'drugapp/view_all_interactions.html',
                              {'msg': 'Drug not found', 'form': GetDrugForm()})
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
                return render(request, 'drugapp/interacting_targets.html',
                              {'msg': 'Drug not found', 'form': GetDrugForm()})
        else:
            return render(request, 'drugapp/interacting_targets.html', {'msg': 'Wrong input', 'form': GetDrugForm()})

        interacting_targets = [{'uniprot_id': t[0], 'name': t[1]} for t in interacting_targets]
        return render(request, 'drugapp/interacting_targets.html',
                      {'form': GetDrugForm(), 'interacting_targets': interacting_targets})


def listDrugs(request):
    drugs = return_drugs()
    drugs_dict = {"drugs_list": drugs}
    return render(request, 'drugapp/list_all_drugs.html', drugs_dict)


def showDrug(request, drugid):
    drug_details = return_drug_details(drugid)
    return render(request, 'drugapp/drug_detail.html', drug_details)


def view_interacting_drugs(request):
    if request.method == 'GET':
        context = {'form': GetProtein()}
        return render(request, 'drugapp/interacting_drugs.html', context)
    elif request.method == 'POST':
        form = GetProtein(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            interacting_drugs = view_interacting_drugs_db(f['uniprot_id'])
            if not interacting_drugs:
                return render(request, 'drugapp/interacting_drugs.html',
                              {'msg': 'Protein not found', 'form': GetProtein()})
        else:
            return render(request, 'drugapp/interacting_drugs.html',
                          {'msg': 'Wrong input', 'form': GetProtein()})

        interacting_drugs = [{'drugbank_id': t[0], 'drug_name': t[1]} for t in interacting_drugs]
        return render(request, 'drugapp/interacting_drugs.html',
                      {'form': GetProtein(), 'interacting_drugs': interacting_drugs})


def get_drugs_of_side_effect(request):
    if request.method == 'GET':
        context = {'form': GetSideEffect()}
        return render(request, 'drugapp/drugs_of_side_effect.html', context)
    elif request.method == 'POST':
        form = GetSideEffect(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            drugs_with_side_effect = view_drugs_of_side_effect_db(f['umls_cui'])
            if not drugs_with_side_effect:
                return render(request, 'drugapp/drugs_of_side_effect.html',
                              {'msg': 'Drug not found', 'form': GetSideEffect()})
        else:
            return render(request, 'drugapp/drugs_of_side_effect.html', {'msg': 'Wrong input', 'form': GetSideEffect()})

        return render(request, 'drugapp/drugs_of_side_effect.html',
                      {'form': GetSideEffect(), 'drugs_with_side_effect': drugs_with_side_effect})


def get_same_protein_drugs(request):
    proteins = {"proteins": get_same_protein_drugs_db()}
    print(proteins)
    return render(request, 'drugapp/same_protein_drugs.html', proteins)


def list_proteins(request):
    proteins = return_proteins()
    proteins_dict = {"proteins_list": proteins}
    return render(request, 'drugapp/list_all_proteins.html', proteins_dict)


def list_side_effects(request):
    side_effects = return_side_effects()
    side_effects_dict = {"side_effects_list": side_effects}
    return render(request, 'drugapp/list_all_side_effects.html', side_effects_dict)
