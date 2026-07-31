from django.contrib import admin
from .models import Airport


# Register the Airport model with the Django admin site
@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    # Columns displayed in the admin list view
    list_display = (
        "code",
        "duration",
        "left",
        "right",
    )

    # Enable searching airports by their code
    search_fields = ("code",)
