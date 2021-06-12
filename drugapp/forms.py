from django import forms

class ReactionAffinityEditForm(forms.Form):
    reaction_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Reaction ID'}))
    affinity = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Affinity'}))