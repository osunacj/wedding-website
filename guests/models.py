from __future__ import unicode_literals
import uuid

from django.db import models

# these will determine the default formality of correspondence
ALLOWED_TYPES = [
    ('formal', 'formal'),
    ('fun', 'fun'),
    ('dimagi', 'dimagi'),
]


def _random_uuid():
    # No longer used by any current field (it used to default Party.invitation_id,
    # which has been removed along with the rest of the invitation system) -
    # but several historical migrations still import this by dotted path as a
    # stored field default, so it has to stay for `migrate` to replay cleanly
    # on a fresh database.
    return uuid.uuid4().hex


class Party(models.Model):
    """
    A party consists of one or more guests.
    """
    name = models.TextField()
    type = models.CharField(max_length=10, choices=ALLOWED_TYPES)
    category = models.CharField(max_length=20, null=True, blank=True)
    is_invited = models.BooleanField(default=False)
    rehearsal_dinner = models.BooleanField(default=False)
    is_attending = models.BooleanField(default=None, null=True)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Party: {}'.format(self.name)

    @classmethod
    def in_default_order(cls):
        return cls.objects.order_by('category', '-is_invited', 'name')

    @property
    def ordered_guests(self):
        return self.guest_set.order_by('is_child', 'pk')

    @property
    def any_guests_attending(self):
        return any(self.guest_set.values_list('is_attending', flat=True))

    @property
    def guest_emails(self):
        return list(filter(None, self.guest_set.values_list('email', flat=True)))


MEALS = [
    ('beef', 'cow'),
    ('fish', 'fish'),
    ('hen', 'hen'),
    ('vegetarian', 'vegetable'),
]


class Guest(models.Model):
    """
    A single guest
    """
    party = models.ForeignKey('Party', on_delete=models.CASCADE)
    first_name = models.TextField()
    last_name = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    is_attending = models.BooleanField(default=None, null=True)
    meal = models.CharField(max_length=20, choices=MEALS, null=True, blank=True)
    is_child = models.BooleanField(default=False)

    @property
    def name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    @property
    def unique_id(self):
        # convert to string so it can be used in the "add" templatetag
        return str(self.pk)

    def __str__(self):
        return 'Guest: {} {}'.format(self.first_name, self.last_name)


class RSVP(models.Model):
    """
    A general, public RSVP submitted through the homepage form. Anyone can
    submit one of these, independent of the Party/Guest guest list.
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30, blank=True)
    is_attending = models.BooleanField()
    # only meaningful when is_attending is True
    guest_count = models.PositiveSmallIntegerField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        if self.is_attending:
            return '{} (attending, {} guest{})'.format(
                self.full_name, self.guest_count, '' if self.guest_count == 1 else 's'
            )
        return '{} (not attending)'.format(self.full_name)
