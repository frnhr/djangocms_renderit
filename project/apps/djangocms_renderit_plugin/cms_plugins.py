from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.template.base import Template
from django.conf import settings
from .models import RenderitCMSPlugin


TEMPLATE = (
    '{% load cms_tags renderit_tags #ADDITIONAL_LIBRARIES# %}'
    '{% for plugin in instance.child_plugin_instances %}'
    '{% renderit %}{% renderit_plugin plugin "#ADDITIONAL_LIBRARIES#" %}{% endrenderit %}'
    '{% endfor %}')


ERROR_TEMPLATE = ('<div style="'
                  'max-height: 300px; '
                  'max-width: 100%; '
                  'overflow: auto; '
                  'padding: 5px; '
                  'background: #eee;"'
                  '>'
                  '    <span style="color: red;">{message}</span>'
                  '    {output_html}'
                  '</div>')

ERROR_OUTPUT_TEMPLATE = '<div style="border: 1px dotted red; padding: 0;">{}</div>'


class RenderItPlugin(CMSPluginBase):
    model = RenderitCMSPlugin
    cache = False
    allow_children = True

    def get_render_template(self, context, instance, placeholder):
        try:
            libraries = ' '.join(map(str, settings.CMS_RENDERIT_TAG_LIBRARIES))
        except AttributeError:
            libraries = ''
        if instance.tag_libraries:
            libraries = ' '.join((libraries, instance.tag_libraries))
        try:
            return Template(TEMPLATE.replace('#ADDITIONAL_LIBRARIES#', libraries))
        except Exception as e:
            return Template(render_exception(e))


plugin_pool.register_plugin(RenderItPlugin)


def render_exception(e, output=None):
    return ERROR_TEMPLATE.format(
        message=str(e),
        output_html='' if not output else ERROR_OUTPUT_TEMPLATE.format(output),
    )