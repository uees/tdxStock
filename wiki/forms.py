from django import forms
from django.conf import settings
from django.template import loader

from .models import Concept


class MarkdownWidget(forms.Textarea):

    def __init__(self, *args, **kwargs):
        self.template = kwargs.pop('template', 'widgets/editor_md.html')
        self.lib = settings.STATIC_URL + "editor.md/lib/"
        self.width = kwargs.pop("width", "100%")
        self.height = kwargs.pop("height", "640")
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(attrs, {'name': name})

        if "class" not in final_attrs:
            final_attrs["class"] = ""
        final_attrs["class"] += " wmd-input"
        template = loader.get_template(self.template)
        markdown_conf = {
            'width': self.width,
            'height': self.height,
            'path': self.lib,
            'id': final_attrs["id"],
        }
        context = self.get_context(name, value, attrs)
        context.update(markdown_conf)
        return template.render(context)

    class Media:
        css = {
            "all": ("css/editormd.min.css",)
        }
        js = (
            'js/editormd.min.js',
        )


class ConceptForm(forms.ModelForm):
    name = forms.CharField(label='名词', required=True, widget=forms.TextInput(
        attrs={'value': "", 'size': "30", 'maxlength': "245", 'aria-required': 'true'}))
    description = forms.CharField(label='解释', required=True)

    class Meta:
        model = Concept
        fields = ['name', 'description']
