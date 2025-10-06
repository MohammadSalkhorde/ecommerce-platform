from django import forms

class CouponForm(forms.Form):
    coupon_code=forms.CharField(label='',
                                widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کد تخفیف','style':'width: 200px;'}),
                                error_messages={'required':'این فیلد نمی تواند خالی باشد'})