from django.db import models


class Airport(models.Model):
    # Unique airport code (e.g., "DEL", "DXB", "JFK")
    code = models.CharField(
        max_length=10,
        unique=True
    )

    # Time required to stay/travel at this airport (in minutes)
    duration = models.IntegerField(
        help_text="Duration in minutes"
    )

    # Reference to the left child airport in the tree
    # SET_NULL keeps the record even if the referenced airport is deleted
    left = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,          # Database can store NULL
        blank=True,         # Optional in Django forms/admin
        related_name='left_parent'
    )

    # Reference to the right child airport in the tree
    right = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='right_parent'
    )

    # String representation shown in Django admin and shell
    def __str__(self):
        return self.code