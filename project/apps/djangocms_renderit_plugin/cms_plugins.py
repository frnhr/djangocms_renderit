from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
# from django.utils.translation import ugettext_lazy as _


class RenderItPlugin(CMSPluginBase):
    model = CMSPlugin
    render_template = "renderit_plugin/renderit_plugin.html"
    cache = False


plugin_pool.register_plugin(RenderItPlugin)
