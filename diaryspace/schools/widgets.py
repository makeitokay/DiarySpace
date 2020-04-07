from django.forms import widgets


class BootstrapCheckboxSelectMultiple(widgets.CheckboxSelectMultiple):
    template_name = "schools/widgets/bootstrap_checkbox_select_multiple.html"
    option_template_name = "schools/widgets/bootstrap_checkbox_select_multiple_option.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs["class"] = self.attrs.get("class", "") + " custom-control-input"
