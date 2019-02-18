import json

from django.forms import Widget
from django.utils.safestring import mark_safe


class JsonEditorWidget(Widget):
    """
    在 django  admin 后台中使用  jsoneditor 处理 JSONField
    """

    html_template = """
    <div id='%(name)s_editor_holder' style='padding-left:170px'></div>
    <textarea hidden readonly class="vLargeTextField" cols="40" id="id_%(name)s" name="%(name)s" rows="20">%(value)s</textarea>
    <script type="text/javascript">
        var element = document.getElementById('%(name)s_editor_holder');
        var json_value = %(value)s;
        var %(name)s_editor = new JSONEditor(element, {
            onChange: function() {
                var textarea = document.getElementById('id_%(name)s');
                var json_changed = JSON.stringify(%(name)s_editor.get()['Object']);
                textarea.value = json_changed;
            }
        });
        %(name)s_editor.set({"Object": json_value})
        %(name)s_editor.expandAll()
    </script>
    """

    def render(self, name, value, attrs=None, renderer=None):
        if isinstance(value, str):
            value = json.loads(value)

        result = self.html_template % {'name': name, 'value': json.dumps(value)}

        return mark_safe(result)
