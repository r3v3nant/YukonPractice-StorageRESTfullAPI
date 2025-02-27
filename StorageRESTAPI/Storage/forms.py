from django import forms
from .models import Products, ProdCategories
from PIL import Image

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'category', 'image', 'preview']

    def clean_image(self): #Перевіряє, що image не перевищує 10MB
        image = self.cleaned_data.get('image')
        if image:
            max_size = 10 * 1024 * 1024  # 10MB у байтах
            if image.size > max_size:
                raise forms.ValidationError("Max Size - 10MB.")
        return image

    def clean_preview(self): #Перевіряє, що preview не перевищує 100x100 пікселів
        preview = self.cleaned_data.get('preview')

        if not preview.name.lower().endswith('.png'):
            raise forms.ValidationError('Preview should be ".png"!')

        if preview:
            image = Image.open(preview)
            width, height = image.size

            if width > 100 or height > 100:
                raise forms.ValidationError("Max size is 100x100 pixels!")
        return preview

class ProductFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        label="Find Product",
        widget=forms.TextInput(attrs={"placeholder": "Input product name..."})
    )
    category = forms.ModelChoiceField(
        queryset=ProdCategories.objects.all(),
        required=False,
        label="Category",
        empty_label="Categories"
    )

class ProdCategoryForm(forms.ModelForm):
    class Meta:
        model = ProdCategories
        fields = ['name']