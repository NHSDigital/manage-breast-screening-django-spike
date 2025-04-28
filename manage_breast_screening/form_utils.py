from dataclasses import dataclass
from typing import Any, Type

from django.forms import Form


@dataclass
class Step:
    """
    A step in the wizard with no form attached
    """

    id: str
    title: str
    template = "wizard_step.jinja"

    def is_final(self):
        return True


@dataclass
class ChoiceStep[F: Form](Step):
    """
    A step with a form and a choice at the end
    """

    form_class: Type[F]
    continue_step: Step
    dropout_step: Step
    next_step_legend: str
    continue_label: str
    dropout_label: str
    next_step_hint: str = ""
    field_name: str = "next_step"
    field_value_continue: Any = True

    def is_final(self):
        return False

    def next_step(self, form: F):
        if self.field_name not in form.cleaned_data:
            raise ValueError(f"Invalid form: missing {self.field_name} value")

        if form.cleaned_data[self.field_name] == self.field_value_continue:
            return self.continue_step
        else:
            return self.dropout_step


class Wizard:
    """
    A tree like structure containing steps.
    """

    def __init__(self, start_step: Step):
        self.steps: dict[str, Step] = {}
        self.start_step = start_step
        self._traverse_tree(start_step)

    def _traverse_tree(self, step: Step):
        self.steps[step.id] = step
        match step:
            case ChoiceStep(continue_step=continue_step, dropout_step=dropout_step):
                if continue_step.id not in self.steps:
                    self._traverse_tree(continue_step)
                if dropout_step.id not in self.steps:
                    self._traverse_tree(dropout_step)

    def get_step_by_id(self, id):
        return self.steps[id]
