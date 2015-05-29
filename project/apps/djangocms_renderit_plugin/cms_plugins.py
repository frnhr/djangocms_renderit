from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin


class RenderItPlugin(CMSPluginBase):
    model = CMSPlugin
    render_template = "renderit_plugin/renderit_plugin.html"
    cache = False
    allow_children = True


plugin_pool.register_plugin(RenderItPlugin)
