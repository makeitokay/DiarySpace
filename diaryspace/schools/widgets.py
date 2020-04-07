from django.forms import widgets


class BootstrapCheckboxSelectMultiple(widgets.CheckboxSelectMultiple):
    template_name = "schools/widgets/bootstrap_checkbox_select_multiple.html"
    option_template_name = "schools/widgets/bootstrap_checkbox_select_multiple_option.html"
