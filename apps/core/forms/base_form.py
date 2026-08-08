from django import forms


class BaseStyledModelForm(forms.ModelForm):
    """
    Formulario base del sistema.

    Aplica automáticamente los estilos institucionales
    definidos para Bootstrap.
    """

    TEXTAREA_ROWS = 4

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            widget = field.widget

            if isinstance(widget, forms.Select):

                css_class = "form-select"

            elif isinstance(widget, forms.CheckboxInput):

                css_class = "form-check-input"

            else:

                css_class = "form-control"

            existing_classes = widget.attrs.get("class", "")

            if css_class not in existing_classes.split():

                widget.attrs["class"] = (

                    f"{existing_classes} {css_class}"

                ).strip()

            if not isinstance(widget, forms.CheckboxInput):

                widget.attrs.setdefault(

                    "autocomplete",

                    "off",

                )


    def _remove_fields(self, *field_names):

        for name in field_names:

            self.fields.pop(

                name,

                None,

            )