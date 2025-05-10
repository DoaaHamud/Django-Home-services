from django import forms
from .models import Order
from .models import*

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['description']
        labels = {
            'description': 'وصف المشكلة',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'صف المشكلة بالتفصيل'}),
        }

class AdminOrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']  # فقط حقل الحالة
        labels = {
            'status': 'حالة الطلب',
        }        
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars']
        labels = {
            'stars': 'التقييم (عدد النجوم)',
            # 'comment': 'تعليقك',
        }
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            # 'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'اكتب تعليقك عن الطلب أو الخدمة'}),
        }

        


