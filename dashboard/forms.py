from django import forms
from django.forms import inlineformset_factory

from .models import Announcement, AppearanceSetting, Location


class LocationStateForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["is_closed"]
        widgets = {
            "is_closed": forms.CheckboxInput(attrs={"class": "toggle-input"}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["text", "is_active", "is_important"]
        widgets = {
            "text": forms.TextInput(attrs={"placeholder": "Nowy komunikat"}),
            "is_active": forms.CheckboxInput(attrs={"class": "toggle-input"}),
            "is_important": forms.CheckboxInput(attrs={"class": "toggle-input"}),
        }


AnnouncementFormSet = inlineformset_factory(
    Location,
    Announcement,
    form=AnnouncementForm,
    extra=1,
    can_delete=True,
)


class AppearanceSettingsForm(forms.Form):
    COLOR_FIELDS = {
        "bg_color": "Tło strony",
        "header_color": "Nagłówek",
        "card_text": "Tekst kart",
        "card_overlay": "Nakładka kart",
        "card_open_start": "Gradient otwartej (początek)",
        "card_open_end": "Gradient otwartej (koniec)",
        "card_closed_start": "Gradient zamkniętej (początek)",
        "card_closed_end": "Gradient zamkniętej (koniec)",
        "card_zone_start": "Gradient stref (początek)",
        "card_zone_end": "Gradient stref (koniec)",
        "card_border": "Ramki kart",
        "important_border": "Ramka ważnych komunikatów",
        "button_bg": "Tło przycisków",
        "button_text": "Tekst przycisków",
        "input_bg": "Tło pól",
        "input_text": "Tekst pól",
    }

    def __init__(self, *args, **kwargs):
        initial = kwargs.get("initial") or {}
        palette = AppearanceSetting.default_palette()
        palette.update(initial)
        kwargs["initial"] = palette
        super().__init__(*args, **kwargs)
        for key, label in self.COLOR_FIELDS.items():
            input_type = "color" if key != "card_overlay" else "text"
            self.fields[key] = forms.CharField(
                label=label,
                widget=forms.TextInput(attrs={"type": input_type, "data-color-key": key}),
            )

    def to_palette(self):
        palette = AppearanceSetting.default_palette()
        for key in self.COLOR_FIELDS.keys():
            palette[key] = self.cleaned_data.get(key) or palette[key]
        return palette
