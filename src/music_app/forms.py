from django import forms

class SongLimitForm(forms.Form):
    song_limit = forms.IntegerField(label='Guest song limit:', initial=3, min_value=1, max_value=50)