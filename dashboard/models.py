from django.db import models


class Location(models.Model):
    TRANS = "trans"
    P1 = "p1"
    P2 = "p2"
    P3 = "p3"
    P4 = "p4"
    STREFY = "strefy"

    LOCATION_CHOICES = [
        (TRANS, "TRANS"),
        (P1, "P1"),
        (P2, "P2"),
        (P3, "P3"),
        (P4, "P4"),
        (STREFY, "STREFY"),
    ]

    name = models.CharField(max_length=64)
    slug = models.CharField(max_length=32, unique=True, choices=LOCATION_CHOICES)
    order = models.PositiveIntegerField(default=0)
    is_closed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Announcement(models.Model):
    location = models.ForeignKey(Location, related_name="announcements", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_important", "created_at"]

    def __str__(self):
        return f"{self.location.name}: {self.text}"


class AppearanceSetting(models.Model):
    key = models.CharField(max_length=32, default="default", unique=True)
    data = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def default_palette():
        return {
            "bg_color": "#0b1021",
            "header_color": "#f5f7fb",
            "card_text": "#e6e9ed",
            "card_overlay": "rgba(0, 0, 0, 0.35)",
            "card_open_start": "#1c7d36",
            "card_open_end": "#0c5a24",
            "card_closed_start": "#b81d13",
            "card_closed_end": "#8b0000",
            "card_zone_start": "#1565c0",
            "card_zone_end": "#0d47a1",
            "card_border": "#0a0c12",
            "important_border": "#ff2d2d",
            "button_bg": "#1e2538",
            "button_text": "#f2f4f8",
            "input_bg": "#111728",
            "input_text": "#e2e5ee",
        }

    def save(self, *args, **kwargs):
        if not self.data:
            self.data = self.default_palette()
        else:
            palette = self.default_palette()
            palette.update(self.data)
            self.data = palette
        super().save(*args, **kwargs)

    def __str__(self):
        return "Appearance settings"
