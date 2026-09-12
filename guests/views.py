from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from guests import csv_import
from guests.forms import RSVPForm
from guests.models import Guest, Party


def home(request):
    rsvp_submitted = False
    if request.method == 'POST':
        rsvp_form = RSVPForm(request.POST)
        if rsvp_form.is_valid():
            rsvp_form.save()
            # redirect so a page refresh doesn't resubmit the form
            return HttpResponseRedirect(reverse('home') + '?rsvp=submitted#rsvp')
    else:
        rsvp_form = RSVPForm()
        rsvp_submitted = request.GET.get('rsvp') == 'submitted'
    return render(request, 'home.html', context={
        'support_email': settings.DEFAULT_WEDDING_REPLY_EMAIL,
        'website_url': settings.WEDDING_WEBSITE_URL,
        'couple_name': settings.BRIDE_AND_GROOM,
        'wedding_location': settings.WEDDING_LOCATION,
        'wedding_date': settings.WEDDING_DATE,
        'rsvp_form': rsvp_form,
        'rsvp_submitted': rsvp_submitted,
    })


class GuestListView(ListView):
    model = Guest


@login_required
def export_guests(request):
    export = csv_import.export_guests()
    response = HttpResponse(export.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=all-guests.csv'
    return response


@login_required
def dashboard(request):
    parties_with_pending_invites = Party.objects.filter(
        is_invited=True, is_attending=None
    ).order_by('category', 'name')
    attending_guests = Guest.objects.filter(is_attending=True)
    guests_without_meals = attending_guests.filter(
        is_child=False
    ).filter(
        Q(meal__isnull=True) | Q(meal='')
    ).order_by(
        'party__category', 'first_name'
    )
    meal_breakdown = attending_guests.exclude(meal=None).values('meal').annotate(count=Count('*'))
    category_breakdown = attending_guests.values('party__category').annotate(count=Count('*'))
    return render(request, 'guests/dashboard.html', context={
        'couple_name': settings.BRIDE_AND_GROOM,
        'website_url': settings.WEDDING_WEBSITE_URL,
        'guests': Guest.objects.filter(is_attending=True).count(),
        'possible_guests': Guest.objects.filter(party__is_invited=True).exclude(is_attending=False).count(),
        'not_coming_guests': Guest.objects.filter(is_attending=False).count(),
        'pending_invites': parties_with_pending_invites.count(),
        'pending_guests': Guest.objects.filter(party__is_invited=True, is_attending=None).count(),
        'guests_without_meals': guests_without_meals,
        'meal_breakdown': meal_breakdown,
        'category_breakdown': category_breakdown,
        'guestlist': Guest.objects.filter(is_attending=True),
        'notcoming': Guest.objects.filter(is_attending=False),
    })
