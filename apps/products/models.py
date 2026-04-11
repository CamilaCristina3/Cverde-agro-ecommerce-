from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("Frutas", "Frutas"),
        ("Legumes", "Legumes"),
        ("Verduras", "Verduras"),
        ("Hortaliças", "Hortaliças"),
        ("Grãos", "Grãos"),
        ("Orgânicos", "Orgânicos"),
    ]

    producer = models.ForeignKey(
        "producers.Producer",
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)
    unit = models.CharField(max_length=20, default="kg")
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    is_organic = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.producer})"

    @property
    def image_class(self) -> str:
        return slugify(self.name)
