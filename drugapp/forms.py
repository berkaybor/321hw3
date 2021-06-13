from django import forms

class ReactionAffinityEditForm(forms.Form):
    reaction_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Reaction ID'}))
    affinity = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Affinity'}))

class GetDrugForm(forms.Form):
    drug_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'DrugBank ID'}))

class GetProtein(forms.Form):
    uniprot_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'UniProt ID'}))

class GetSideEffect(forms.Form):
    umls_cui = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'UMLS CUI'}))