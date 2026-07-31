from django import forms
from .models import Airport


# Form for adding a new airport to the binary tree
class AddAirportForm(forms.Form):

    # Select the parent airport (optional for the root node)
    parent = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        required=False,
        label="Parent Airport (leave blank for root)"
    )

    # Available positions relative to the parent
    POSITION_CHOICES = [
        ('left', 'Left'),
        ('right', 'Right'),
    ]

    # Select whether the new airport should be the left or right child
    position = forms.ChoiceField(
        choices=POSITION_CHOICES,
        required=False,
        label="Position (if parent selected)"
    )

    # Airport code (must be unique)
    code = forms.CharField(
        max_length=10,
        label="Airport Code"
    )

    # Duration in minutes
    duration = forms.IntegerField(
        min_value=0,
        label="Duration (minutes)"
    )

    # Custom validation for the form
    def clean(self):
        # Run Django's default validation first
        cleaned_data = super().clean()

        parent = cleaned_data.get('parent')
        position = cleaned_data.get('position')
        code = cleaned_data.get('code')

        # If a parent is selected, a position must also be selected
        if parent and not position:
            raise forms.ValidationError(
                "Please select a position (Left/Right) when a parent is chosen."
            )

        # A root node should not have a position
        if not parent and position:
            raise forms.ValidationError(
                "Position should not be selected if no parent is chosen (root node)."
            )

        # Ensure the airport code is unique
        if Airport.objects.filter(code=code).exists():
            raise forms.ValidationError(
                f"Airport with code '{code}' already exists."
            )

        # Ensure the selected child position is available
        if parent:
            if position == 'left' and parent.left:
                raise forms.ValidationError(
                    f"{parent.code} already has a left child."
                )

            if position == 'right' and parent.right:
                raise forms.ValidationError(
                    f"{parent.code} already has a right child."
                )

        # Return the validated data
        return cleaned_data
    
# Form for searching a route from a selected airport
class SearchForm(forms.Form):

    # Select the airport where the search begins
    start_airport = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        label="Starting Airport"
    )

    # Available traversal directions
    DIRECTION_CHOICES = [
        ('left', 'Left'),
        ('right', 'Right'),
    ]

    # Select the direction to traverse from the starting airport
    direction = forms.ChoiceField(
        choices=DIRECTION_CHOICES,
        label="Direction"
    )