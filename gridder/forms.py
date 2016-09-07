from django.forms import ModelForm, Select, NumberInput, TextInput
from .models import Grid

from honeypot.fields import Honeypot

from billing.utils import validate_plan

class GridForm(ModelForm):
    message = Honeypot()

    class Meta:
        model = Grid

        fields = (
            'message',
            'width', 'width_unit',
            'height', 'height_unit',
            'margin_left', 'margin_left_unit',
            'margin_right', 'margin_right_unit',
            'margin_top', 'margin_top_unit',
            'margin_bottom', 'margin_bottom_unit',
            'columns', 'columns_color', 'columns_opacity',
            'columns_gutter', 'columns_gutter_unit',
            'baseline', 'baseline_unit',
            'baseline_color', 'baseline_opacity',

        )

        widgets = {
            'width': NumberInput(attrs={'class': 'value form-control input-sm'}),
            'width_unit': Select(attrs={'class': 'units form-control input-sm'}),
            'height': NumberInput(attrs={'class': 'value form-control input-sm'}),
            'height_unit': Select(attrs={'class': 'units form-control input-sm'}),
            'margin_left': NumberInput(attrs={'class': 'value form-control input-sm'}),
            'margin_left_unit': Select(attrs={'class': 'units form-control input-sm'}),
            'margin_right': NumberInput(attrs={'class': 'value form-control input-sm'}),
            'margin_right_unit': Select(attrs={'class': 'units form-control input-sm'}),
            'margin_top': NumberInput(attrs={'class': 'value form-control input-sm'}),
            'margin_top_unit': Select(attrs={'class': 'units form-control input-sm'}),
            'margin_bottom': NumberInput(attrs={'class': 'value form-control input-sm'}),
            'margin_bottom_unit': Select(attrs={'class': 'units form-control input-sm'}),
            'columns_color': TextInput(attrs={'class': 'value form-control input-sm'}),
            'columns_opacity': NumberInput(attrs={'class': 'value form-control input-sm'}),
            'baseline_color': TextInput(attrs={'class': 'value form-control input-sm'}),
            'baseline_opacity': NumberInput(attrs={'class': 'value form-control input-sm'}),
            'columns_gutter': NumberInput(attrs={'class': 'value form-control input-sm'}),
            'columns_gutter_unit': Select(attrs={'class': 'units form-control input-sm'}),
            'columns': NumberInput(attrs={'class': 'value form-control input-sm'}),
            'baseline': NumberInput(attrs={'class': 'value form-control input-sm'}),
            'baseline_unit': Select(attrs={'class': 'units form-control input-sm'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(GridForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(GridForm, self).clean()
        validate_plan(cleaned_data['user'], add=1, request=self.request)
        return cleaned_data
