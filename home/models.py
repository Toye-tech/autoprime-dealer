from django.db import models

class Car(models.Model):
    BADGE_CHOICES = [
        ('new', 'New Arrival'),
        ('hot', 'Hot'),
        ('deal', 'Best Deal'),
        ('', 'No Badge'),
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
    ]
    CATEGORY_CHOICES = [
        ('suv', 'SUV / Crossover'),
        ('sedan', 'Sedan'),
        ('luxury', 'Luxury'),
        ('sport', 'Sports Car'),
        ('pickup', 'Pickup / Truck'),
        ('van', 'Van / Minibus'),
    ]

    brand        = models.CharField(max_length=100)
    model        = models.CharField(max_length=200)
    year         = models.IntegerField()
    category     = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    fuel         = models.CharField(max_length=50, default='Petrol')
    transmission = models.CharField(max_length=50, default='Automatic')
    mileage      = models.IntegerField(default=0)
    colour       = models.CharField(max_length=50, blank=True)
    price        = models.BigIntegerField()
    price_note   = models.CharField(max_length=100, blank=True)
    badge        = models.CharField(max_length=10, choices=BADGE_CHOICES, blank=True)
    featured     = models.BooleanField(default=False)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    image_url    = models.URLField(max_length=500, blank=True)
    wa_message   = models.CharField(max_length=300, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', '-created_at']

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

    def formatted_price(self):
        return f"₦{self.price:,}"