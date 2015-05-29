from django import template
from django.template.base import Template
from apps.djangocms_renderit_plugin.cms_plugins import render_exception

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
        except Exception as e:
            return render_exception(e, output)


register.tag('renderit', do_renderit)
