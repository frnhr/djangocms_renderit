from django import template
from django.template.base import Template

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
        return Template(output).render(context)


register.tag('renderit', do_renderit)
