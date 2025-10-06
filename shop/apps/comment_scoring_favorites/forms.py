from django import forms

class CommentForm(forms.Form):
    product_id=forms.CharField(widget=forms.HiddenInput(), required=False)
    comment_id=forms.CharField(widget=forms.HiddenInput(), required=False)
    comment_text=forms.CharField(label='',
                                 error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                                 widget=forms.Textarea(attrs={'class':'form-control','placeholder':'متن نظر','rows':"4"}))