from django import forms

class FriendMgmtForm(forms.Form):
    friend = forms.CharField(max_length=100,required=False)