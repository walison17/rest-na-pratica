from django.forms.renderers import DjangoTemplates


class BootstrapRenderer(DjangoTemplates):
    form_template_name = "core/snippets/bs_form.html"
