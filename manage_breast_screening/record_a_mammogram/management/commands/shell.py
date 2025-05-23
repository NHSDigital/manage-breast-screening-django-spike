from django.core.management.commands import shell
from django.forms import Form


class Command(shell.Command):
    def get_auto_imports(self):
        """
        Automatically import all form subclasses
        """
        from manage_breast_screening.record_a_mammogram import forms

        extra_imports = [
            f"manage_breast_screening.record_a_mammogram.forms.{name}"
            for name, value in vars(forms).items()
            if isinstance(value, type) and issubclass(value, Form)
        ]

        return super().get_auto_imports() + extra_imports
