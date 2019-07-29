from django import forms


class EditorForm(forms.Form):
    """エディタ部分となるフォーム."""
    code = forms.CharField(
        widget=forms.Textarea,
    )
