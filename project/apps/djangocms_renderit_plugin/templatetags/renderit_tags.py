from django import template
from django.template.base import Template, TemplateSyntaxError


register = template.Library()


def do_renderit(parser, token):
    nodelist = parser.parse(('endrenderit',))
    parser.delete_first_token()
    return RenderNode(nodelist)


class RenderNode(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        try:
            return Template(output).render(context)
        except TemplateSyntaxError as e:
            return self.render_exception(e, output)

    def render_exception(self, e, output):
        # template_source = escape(linebreaksbr(e.django_template_source[0].source))
        return ('<div style="'
                'max-height: 300px; '
                'max-width: 100%; '
                'overflow: auto; '
                'padding: 5px; '
                'background: #eee;"'
                '>'
                '    <span style="color: red;">{message}</span>'
                '    <div style="border: 1px dotted red; padding: 0;">{output}</div>'
                '</div>'
                ''.format(
            message=str(e),
            output=output,
        ))


register.tag('renderit', do_renderit)
