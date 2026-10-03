from django.urls import path, re_path

from guests.views import GuestListView, home, export_guests, dashboard, gift_account

urlpatterns = [
    re_path(r'^$', home, name='home'),
    path('gift-accounts/<int:index>/', gift_account, name='gift-account'),
    re_path(r'^guests/$', GuestListView.as_view(), name='guest-list'),
    re_path(r'^dashboard/$', dashboard, name='dashboard'),
    re_path(r'^guests/export$', export_guests, name='export-guest-list'),
]
