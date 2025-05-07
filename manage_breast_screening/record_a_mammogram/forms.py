from django import forms

class ScreeningAppointmentForm(forms.Form):
    decision = forms.ChoiceField(
        choices=(
            ("continue", "Yes, go to medical information"),
            ("dropout", "No, screening cannot proceed"),
        ),
        required=True,
        widget=forms.RadioSelect(),
    )

    def save(self):
        pass


class AskForMedicalInformationForm(forms.Form):
    decision = forms.ChoiceField(
        choices=(
            ("continue", "Yes, mark incomplete sections as ‘none’ or ‘no’"),
            ("dropout", "No, screening cannot proceed"),
        ),
        required=True,
        widget=forms.RadioSelect(),
    )

    def save(self):
        pass


class RecordMedicalInformationForm(forms.Form):
    decision = forms.ChoiceField(
        choices=(
            ("continue", "Yes, go to medical information"),
            ("dropout", "No, screening cannot proceed"),
        ),
        required=True,
        widget=forms.RadioSelect(),
    )

    def save(self):
        pass


class AppointmentCannotGoAheadForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

    participant_did_not_attend = forms.BooleanField(required=False, label="Participant did not attend")
    participant_did_not_attend_details = forms.CharField(required=False)

    failed_identity_check = forms.BooleanField(required=False, label="Failed identity check")
    failed_identity_check_details = forms.CharField(required=False)

    language_difficulties = forms.BooleanField(required=False, label="Language difficulties")
    language_difficulties_details = forms.CharField(required=False)

    physical_health_issue = forms.BooleanField(required=False, label="Physical health issue")
    physical_health_issue_details = forms.CharField(required=False)

    mental_health_issue = forms.BooleanField(required=False, label="Mental health issue")
    mental_health_issue_details = forms.CharField(required=False)

    last_mammogram_within_6_months = forms.BooleanField(required=False, label="Last mammogram within 6 months")
    last_mammogram_within_6_months_details = forms.CharField(required=False)

    breast_implant_risks = forms.BooleanField(required=False, label="Breast implant risks")
    breast_implant_risks_details = forms.CharField(required=False)

    pain_during_screening = forms.BooleanField(required=False, label="Pain during screening")
    pain_during_screening_details = forms.CharField(required=False)

    technical_issues = forms.BooleanField(required=False, label="Technical issues")
    technical_issues_details = forms.CharField(required=False)

    participant_withdrew_consent = forms.BooleanField(required=False, label="Participant withdrew consent")
    participant_withdrew_consent_details = forms.CharField(required=False)

    other = forms.BooleanField(required=False, label="Other")
    other_details = forms.CharField(required=False)

    decision = forms.ChoiceField(
        choices=(
            ("True", "Yes, add participant to reinvite list"),
            ("False", "No"),
        ),
        required=True,
        widget=forms.RadioSelect(),
    )

    def get_reason_fields(self):
        """Returns a list of tuples containing (field_name, field) for boolean fields that represent reasons"""
        return [(name, field) for name, field in self.fields.items()
                if isinstance(field, forms.BooleanField) and not name.endswith('_details')]

    def save(self):
        if not self.instance:
            raise ValueError("Cannot save form without an Appointment instance")

        stopped_reasons = {}
        for field_name, value in self.cleaned_data.items():
            if field_name == "decision":
                continue
            if value:
                stopped_reasons[field_name] = value
        self.instance.stopped_reasons = stopped_reasons
        self.instance.reinvite = self.cleaned_data["decision"]
        self.instance.status = self.instance.Status.ATTENDED_NOT_SCREENED
        self.instance.save()

        return self.instance