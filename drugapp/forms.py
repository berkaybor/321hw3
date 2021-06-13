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

class GetAuthorsForm(forms.Form):
    reaction_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Reaction ID'}))
    author_names = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'For example: Han, M; Song, C; Jeong, N; Hahn, HG'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class GetKeyword(forms.Form):
    keyword = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search for drugs'}))
