from django import forms

from guests.models import RSVP

# Flat 1-5 for now, open to anyone. Planned: once every guest has an id,
# cap this per-submission to that guest/party's allowed count instead of a
# fixed 5 (e.g. build the choice list from Party/Guest data in the view and
# pass it in here rather than using this fixed list).
_NUMBER_WORDS = ['One', 'Two', 'Three', 'Four', 'Five']
GUEST_COUNT_CHOICES = [(str(n), word) for n, word in enumerate(_NUMBER_WORDS, start=1)]

ATTENDING_CHOICES = [
    ('yes', 'Accept with pleasure'),
    ('no', 'Regretfully decline'),
]


class RSVPForm(forms.ModelForm):
    is_attending = forms.ChoiceField(choices=ATTENDING_CHOICES, widget=forms.RadioSelect)
    guest_count = forms.ChoiceField(choices=GUEST_COUNT_CHOICES, required=False, widget=forms.RadioSelect)

    class Meta:
        model = RSVP
        # is_attending is deliberately left out here: the form's version of
        # it is a yes/no ChoiceField (for the radio buttons) rather than the
        # model's actual BooleanField, and leaving it in Meta.fields makes
        # ModelForm copy that raw "yes"/"no" string onto the model instance
        # and validate it as a BooleanField before save() gets to convert
        # it, which fails. save() below sets it explicitly instead.
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'guest_count']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control', 'required': 'required',
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control', 'required': 'required',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control', 'required': 'required',
        })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
        })
        # is_attending and guest_count are both rendered by hand in the
        # template as bordered "option card" radios, not via this widget,
        # so they don't need form-control attrs here.

    def clean(self):
        cleaned_data = super().clean()
        attending = cleaned_data.get('is_attending') == 'yes'
        if attending and not cleaned_data.get('guest_count'):
            self.add_error('guest_count', 'Please select how many guests will be attending.')
        return cleaned_data

    def save(self, commit=True):
        rsvp = super().save(commit=False)
        rsvp.is_attending = self.cleaned_data['is_attending'] == 'yes'
        rsvp.guest_count = int(self.cleaned_data['guest_count']) if rsvp.is_attending else None
        if commit:
            rsvp.save()
        return rsvp
