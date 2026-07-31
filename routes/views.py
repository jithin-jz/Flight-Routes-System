from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Airport
from .forms import AddAirportForm, SearchForm


# View to display and process the Add Airport form
def add_airport(request):

    # Handle form submission
    if request.method == 'POST':
        form = AddAirportForm(request.POST)

        # Validate the submitted form
        if form.is_valid():

            # Retrieve validated form data
            parent = form.cleaned_data['parent']
            position = form.cleaned_data['position']
            code = form.cleaned_data['code']
            duration = form.cleaned_data['duration']

            # Create the new airport
            airport = Airport.objects.create(
                code=code,
                duration=duration
            )

            # Attach the airport to the selected parent
            if parent:
                if position == 'left':
                    parent.left = airport
                else:
                    parent.right = airport

                # Save the updated parent node
                parent.save()

            # Display a success message
            messages.success(
                request,
                f"Airport {code} added successfully."
            )

            # Redirect to prevent duplicate form submission
            return redirect('add_airport')

    # Display an empty form on GET request
    else:
        form = AddAirportForm()

    # Render the template with the form
    return render(
        request,
        'routes/add_airport.html',
        {'form': form}
    )