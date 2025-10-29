from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm


def home(request):
    events = Event.objects.select_related("category").prefetch_related("participants")[
        :9
    ]
    return render(request, "events/home.html", {"events": events})


def event_list(request):
    events = (
        Event.objects.select_related("category").prefetch_related("participants").all()
    )
    categories = Category.objects.all()  # needed for dropdown

    # Search filter
    search_query = request.GET.get("q", "")
    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)
        )

    # Category filter
    category_id = request.GET.get("category")
    if category_id:
        events = events.filter(category_id=category_id)

    # Date range filter
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    if date_from and date_to:
        events = events.filter(date__range=[date_from, date_to])
    elif date_from:
        events = events.filter(date__gte=date_from)
    elif date_to:
        events = events.filter(date__lte=date_to)

    context = {
        "events": events,
        "categories": categories,
    }
    return render(request, "events/event_list.html", context)


def event_detail(request, id):
    event = get_object_or_404(
        Event.objects.select_related("category").prefetch_related("participants"), id=id
    )
    return render(request, "events/event_detail.html", {"event": event})


def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("events:event_list")
    else:
        form = EventForm()
    return render(request, "events/event_form.html", {"form": form, "action": "Create"})


def event_update(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("events:event_list")
    else:
        form = EventForm(instance=event)
    return render(request, "events/event_form.html", {"form": form, "action": "Update"})


def event_delete(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        event.delete()
        return redirect("events:event_list")
    return render(request, "events/confirm_delete.html", {"object": event})


def dashboard(request):
    today = timezone.localdate()

    # Counts
    total_participants = Participant.objects.count()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=today).count()
    past_events = Event.objects.filter(date__lt=today).count()

    # Today's events
    todays_events = (
        Event.objects.filter(date=today)
        .select_related("category")
        .prefetch_related("participants")
    )

    context = {
        "total_participants": total_participants,
        "total_events": total_events,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "todays_events": todays_events,
    }
    return render(request, "events/dashboard.html", context)


def participant_list(request):
    participants = Participant.objects.prefetch_related("events").all()
    return render(
        request, "events/participant_list.html", {"participants": participants}
    )


def participant_create(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("events:participant_list")
    else:
        form = ParticipantForm()
    return render(
        request, "events/participant_form.html", {"form": form, "action": "Create"}
    )


def participant_update(request, id):
    participant = get_object_or_404(Participant, id=id)
    if request.method == "POST":
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect("events:participant_list")
    else:
        form = ParticipantForm(instance=participant)
    return render(
        request, "events/participant_form.html", {"form": form, "action": "Update"}
    )


def participant_delete(request, id):
    participant = get_object_or_404(Participant, id=id)
    if request.method == "POST":
        participant.delete()
        return redirect("events:participant_list")
    return render(request, "events/confirm_delete.html", {"object": participant})


def category_list(request):
    categories = Category.objects.annotate(event_count=Count("events"))
    return render(request, "events/category_list.html", {"categories": categories})


def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("events:category_list")
    else:
        form = CategoryForm()
    return render(
        request, "events/category_form.html", {"form": form, "action": "Create"}
    )


def category_update(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("events:category_list")
    else:
        form = CategoryForm(instance=category)
    return render(
        request, "events/category_form.html", {"form": form, "action": "Update"}
    )


def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        category.delete()
        return redirect("events:category_list")
    return render(request, "events/confirm_delete.html", {"object": category})
