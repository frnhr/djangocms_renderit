from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.template.base import Template
from django.conf import settings
from .models import RenderitCMSPlugin

TEMPLATE = (
    '{% load cms_tags %}'
    '{% for plugin in instance.child_plugin_instances %}'
    '{% render_plugin plugin %}'
    '{% endfor %}')


class RenderItPlugin(CMSPluginBase):
    model = RenderitCMSPlugin
    cache = False
    allow_children = True

    def get_render_template(self, context, instance, placeholder):
        return Template(TEMPLATE)


plugin_pool.register_plugin(RenderItPlugin)
