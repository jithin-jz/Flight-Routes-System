import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Airport
from .forms import AddAirportForm, SearchForm


def _serialize_airport(airport):
    if not airport:
        return None
    return {
        "id": airport.id,
        "code": airport.code,
        "duration": airport.duration,
        "left": _serialize_airport(airport.left),
        "right": _serialize_airport(airport.right),
    }


# View to display and process the Add Airport form
def add_airport(request):
    # Handle form submission
    if request.method == "POST":
        form = AddAirportForm(request.POST)

        # Validate the submitted form
        if form.is_valid():
            # Retrieve validated form data
            parent = form.cleaned_data["parent"]
            position = form.cleaned_data["position"]
            code = form.cleaned_data["code"]
            duration = form.cleaned_data["duration"]

            # Create the new airport
            airport = Airport.objects.create(code=code, duration=duration)

            # Attach the airport to the selected parent
            if parent:
                if position == "left":
                    parent.left = airport
                else:
                    parent.right = airport

                # Save the updated parent node
                parent.save()

            # Display a success message
            messages.success(request, f"Airport {code} added successfully.")

            # Redirect to prevent duplicate form submission
            return redirect("add_airport")

    # Display an empty form on GET request
    else:
        form = AddAirportForm()

    # Render the template with the form
    return render(request, "routes/add_airport.html", {"form": form})


def search_airport(request):
    result = None
    start_node = None
    direction = None
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            start_node = form.cleaned_data["start_airport"]
            direction = form.cleaned_data["direction"]
            current = start_node
            # Traverse until no further child in that direction
            while True:
                if direction == "left":
                    if current.left:
                        current = current.left
                    else:
                        break
                else:  # right
                    if current.right:
                        current = current.right
                    else:
                        break
            result = current
    else:
        form = SearchForm()
    return render(
        request,
        "routes/search.html",
        {
            "form": form,
            "result": result,
            "start_node": start_node,
            "direction": direction,
        },
    )


def longest_duration(request):
    airport = Airport.objects.order_by("-duration").first()
    return render(request, "routes/longest.html", {"airport": airport})


def shortest_duration(request):
    airport = Airport.objects.order_by("duration").first()
    return render(request, "routes/shortest.html", {"airport": airport})


def home(request):
    add_form = AddAirportForm()
    search_form = SearchForm()
    search_result = None
    search_start_node = None
    search_direction = None
    traversed_path_ids = []

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "add_airport" or "code" in request.POST:
            add_form = AddAirportForm(request.POST)
            if add_form.is_valid():
                parent = add_form.cleaned_data["parent"]
                position = add_form.cleaned_data["position"]
                code = add_form.cleaned_data["code"]
                duration = add_form.cleaned_data["duration"]

                airport = Airport.objects.create(code=code, duration=duration)
                if parent:
                    if position == "left":
                        parent.left = airport
                    else:
                        parent.right = airport
                    parent.save()

                messages.success(request, f"Airport {code} added successfully!")
                return redirect("home")

        elif form_type == "search_airport" or "start_airport" in request.POST:
            search_form = SearchForm(request.POST)
            if search_form.is_valid():
                search_start_node = search_form.cleaned_data["start_airport"]
                search_direction = search_form.cleaned_data["direction"]
                current = search_start_node
                traversed_path_ids.append(current.id)

                while True:
                    if search_direction == "left":
                        if current.left:
                            current = current.left
                            traversed_path_ids.append(current.id)
                        else:
                            break
                    else:  # right
                        if current.right:
                            current = current.right
                            traversed_path_ids.append(current.id)
                        else:
                            break
                search_result = current

    # Fetch stats and tree nodes
    airports = Airport.objects.all().order_by("code")
    total_airports = airports.count()
    longest_airport = Airport.objects.order_by("-duration").first()
    shortest_airport = Airport.objects.order_by("duration").first()

    # Find root nodes (nodes that are not a left or right child of any parent)
    child_ids = set(
        Airport.objects.exclude(left__isnull=True).values_list("left_id", flat=True)
    ) | set(
        Airport.objects.exclude(right__isnull=True).values_list("right_id", flat=True)
    )
    roots = Airport.objects.exclude(id__in=child_ids)
    tree_data = [_serialize_airport(r) for r in roots]

    context = {
        "add_form": add_form,
        "search_form": search_form,
        "airports": airports,
        "total_airports": total_airports,
        "longest_airport": longest_airport,
        "shortest_airport": shortest_airport,
        "search_result": search_result,
        "search_start_node": search_start_node,
        "search_direction": search_direction,
        "traversed_path_ids": json.dumps(traversed_path_ids),
        "tree_data_json": json.dumps(tree_data),
    }

    return render(request, "routes/home.html", context)
