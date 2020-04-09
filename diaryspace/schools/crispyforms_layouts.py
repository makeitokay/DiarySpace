from crispy_forms.layout import BaseInput


class SubclassCustomizableSubmit(BaseInput):
    """
    :cls:`~crispy_forms.layout.Submit` without ``btn-primary``. This allows to set other button
    subclasses such as ``btn-outline-secondary``.
    """

    input_type = "submit"

    def __init__(self, *args, **kwargs):
        self.field_classes = "btn"
        super().__init__(*args, **kwargs)
