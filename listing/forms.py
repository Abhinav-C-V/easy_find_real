from django import forms
from .models import Listing

class AddPropertyForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'  # Include all fields from the Listing model

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price

    def clean_bathrooms(self):
        bathrooms = self.cleaned_data['bathrooms']
        if bathrooms < 0:
            raise forms.ValidationError("Number of bathrooms cannot be negative.")
        return bathrooms

    def clean_sale_type(self):
        sale_type = self.cleaned_data['sale_type']
        valid_sale_types = [choice[0] for choice in Listing.SaleType.choices]
        if sale_type not in valid_sale_types:
            raise forms.ValidationError("Invalid sale type.")
        return sale_type

    def clean_zipcode(self):
        zipcode = self.cleaned_data['zipcode']
        if not zipcode.isdigit() or len(zipcode) <= 5:
            raise forms.ValidationError("Invalid ZIP code. It should be a 5-digit number.")
        return zipcode
    
    def clean_city(self):
        city = self.cleaned_data.get('city')
        if city not in [choice[0] for choice in Listing.CITY_CHOICES]:
            raise forms.ValidationError('Invalid city selection.')
        return city

    def clean_state(self):
        state = self.cleaned_data.get('state')
        if state not in [choice[0] for choice in Listing.STATE_CHOICES]:
            raise forms.ValidationError('Invalid state selection.')
        return state