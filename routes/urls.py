from django.urls import path
from routes import views


# URL patterns for the Flight Routes application
urlpatterns = [
    # Home page
    path("", views.home, name="home"),
    # Add a new airport to the binary tree
    path("add/", views.add_airport, name="add_airport"),
    # Search airports by traversing left or right
    path("search/", views.search_airport, name="search"),
    # Display the route with the longest total duration
    path("longest/", views.longest_duration, name="longest"),
    # Display the route with the shortest total duration
    path("shortest/", views.shortest_duration, name="shortest"),
]
