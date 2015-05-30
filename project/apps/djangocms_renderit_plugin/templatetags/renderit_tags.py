from classytags.arguments import Argument
from classytags.core import Options
from cms.templatetags.cms_tags import RenderPlugin
from django import template
from django.template.base import Template, Context

register = template.Library()


class RenderItPlugin(RenderPlugin):
    name = 'renderit_plugin'
    options = Options(
        Argument('plugin'),
        Argument('additional_libs'),
    )

    TEMPLATE = '''{% load renderit_tags #ADDITONAL_TAGS# %}#CONTENT#'''

    def render_tag(self, context, **kwargs):
        """ Take literal template instead of looking over the filesystem for one. """
        # TODO Not very confident about the cuts made here...
        additional_libs = kwargs.pop('additional_libs', '')
        data = self.get_context(context, **kwargs)
        try:
            t = Template(
                self.TEMPLATE.replace(
                    '#CONTENT#', data['content']
                ).replace(
                    '#ADDITONAL_TAGS#', additional_libs
                ))
            return t.render(Context({}))
        except Exception as e:
            return super().render_tag(context, **kwargs)



register.tag(RenderItPlugin)
