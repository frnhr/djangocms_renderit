from django.test import TestCase

from cms.api import add_plugin
from cms.models import Placeholder

from .cms_plugins import RenderItPlugin


class RenderitPluginTests(TestCase):

    # def test_plugin_context(self):
    #     placeholder = Placeholder.objects.create(slot='test')
    #     model_instance = add_plugin(
    #         placeholder,
    #         RenderItPlugin,
    #         'en',
    #     )
    #     plugin_instance = model_instance.get_plugin_class_instance()
    #     context = plugin_instance.render({}, model_instance, None)
    #     self.assertIn('key', context)
    #     self.assertEqual(context['key'], 'value')

    def test_empty_plugin(self):
        placeholder = Placeholder.objects.create()
        model_instance = add_plugin(
            placeholder,
            RenderItPlugin,
            'en',
        )
        html = model_instance.render_plugin({})
        self.assertEqual(html, '')