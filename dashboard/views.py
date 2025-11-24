from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone

from .forms import AnnouncementFormSet, AppearanceSettingsForm, LocationStateForm
from .models import Announcement, AppearanceSetting, Location


def _get_timestamp():
    timestamps = []
    latest_announcement = Announcement.objects.order_by("-updated_at").first()
    latest_location = Location.objects.order_by("-updated_at").first()
    latest_appearance = AppearanceSetting.objects.order_by("-updated_at").first()
    if latest_announcement:
        timestamps.append(latest_announcement.updated_at)
    if latest_location:
        timestamps.append(latest_location.updated_at)
    if latest_appearance:
        timestamps.append(latest_appearance.updated_at)
    if not timestamps:
        return timezone.now().isoformat()
    return max(timestamps).isoformat()


def dashboard(request):
    locations = Location.objects.order_by("order")
    announcements = {
        loc.slug: loc.announcements.filter(is_active=True).order_by("-is_important", "created_at")
        for loc in locations
    }
    appearance = AppearanceSetting.objects.first()
    palette = appearance.data if appearance else AppearanceSetting.default_palette()
    timestamp = _get_timestamp()
    context = {
        "locations": locations,
        "announcements": announcements,
        "timestamp": timestamp,
        "palette": palette,
    }
    return render(request, "dashboard/home.html", context)


def dashboard_fragment(request):
    locations = Location.objects.order_by("order")
    announcements = {
        loc.slug: loc.announcements.filter(is_active=True).order_by("-is_important", "created_at")
        for loc in locations
    }
    timestamp = _get_timestamp()
    html = render_to_string(
        "dashboard/cards_fragment.html",
        {"locations": locations, "announcements": announcements},
        request=request,
    )
    return JsonResponse({"timestamp": timestamp, "html": html})


def leader_panel(request):
    locations = Location.objects.order_by("order")
    appearance, _ = AppearanceSetting.objects.get_or_create(
        key="default", defaults={"data": AppearanceSetting.default_palette()}
    )

    location_forms = {loc.slug: LocationStateForm(request.POST or None, instance=loc, prefix=loc.slug) for loc in locations}
    formsets = {
        loc.slug: AnnouncementFormSet(request.POST or None, instance=loc, prefix=f"msg-{loc.slug}")
        for loc in locations
    }
    appearance_form = AppearanceSettingsForm(request.POST or None, initial=appearance.data)

    if request.method == "POST":
        is_valid = appearance_form.is_valid()
        for loc in locations:
            is_valid = location_forms[loc.slug].is_valid() and is_valid
            is_valid = formsets[loc.slug].is_valid() and is_valid
        if is_valid:
            for loc in locations:
                location_forms[loc.slug].save()
                formsets[loc.slug].save()
            appearance.data = appearance_form.to_palette()
            appearance.save()
            return redirect("leader_panel")

    context = {
        "locations": locations,
        "location_forms": location_forms,
        "formsets": formsets,
        "appearance_form": appearance_form,
        "palette": appearance.data,
    }
    return render(request, "dashboard/leader_panel.html", context)


def appearance_preview(request):
    appearance = get_object_or_404(AppearanceSetting, key="default")
    locations = Location.objects.order_by("order")
    announcements = {
        loc.slug: loc.announcements.filter(is_active=True).order_by("-is_important", "created_at")
        for loc in locations
    }
    html = render_to_string(
        "dashboard/appearance_preview.html",
        {"locations": locations, "announcements": announcements, "palette": appearance.data},
        request=request,
    )
    return JsonResponse({"html": html, "palette": appearance.data})
