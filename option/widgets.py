from django import forms
from django.template import loader


class JsonEditorWidget(forms.Textarea):

    def __init__(self, *args, **kwargs):
        self.template = kwargs.pop('template', 'widgets/json_editor.html')
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        template = loader.get_template(self.template)
        context = self.get_context(name, value, attrs)
        return template.render(context)

    class Media:
        css = {
            "all": (
                "editor.md/lib/codemirror/lib/codemirror.css",
                "editor.md/lib/codemirror/addon/lint/lint.css",
                "editor.md/lib/codemirror/theme/rubyblue.css",
            )
        }
        js = (
            'js/jsonlint.js',
            'editor.md/lib/codemirror/lib/codemirror.js',
            'editor.md/lib/codemirror/mode/javascript/javascript.js',
            "editor.md/lib/codemirror/addon/lint/lint.js",
            "editor.md/lib/codemirror/addon/lint/json-lint.js"
        )
