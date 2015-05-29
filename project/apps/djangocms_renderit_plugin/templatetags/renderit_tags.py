from django import template
from django.template.base import Template, TemplateSyntaxError
from django.template.defaultfilters import linebreaksbr
from django.utils.html import escape

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
            return self.render_exception(e)

    def render_exception(self, e):
        return ('<div style="'
                'max-height: 300px; '
                'max-width: 100%; '
                'overflow: auto; '
                'color: red; '
                'background: #eee;"'
                '>{message}, in:<br />{source}</div>'.format(
            message=str(e),
            source=escape(linebreaksbr(e.django_template_source[0].source)),
        ))


register.tag('renderit', do_renderit)
