from django.test import TestCase, override_settings
from cms.plugin_rendering import PluginContext
from cms.api import add_plugin
from cms.models import Placeholder
from djangocms_text_ckeditor.cms_plugins import TextPlugin
from .cms_plugins import RenderItPlugin


class RenderitPluginTests(TestCase):

    def test_empty_plugin(self):
        placeholder = Placeholder.objects.create()
        model_instance = add_plugin(
            placeholder,
            RenderItPlugin,
            'en',
        )
        html = model_instance.render_plugin({})
        self.assertEqual('', html)

    def test_simple_text_plugin(self):
        placeholder = Placeholder.objects.create()
        renderit_instance = add_plugin(
            placeholder,
            RenderItPlugin,
            'en',
        )
        text_instance = add_plugin(
            placeholder,
            TextPlugin,
            'en',
            body='just some text',
        )
        renderit_instance.child_plugin_instances = [text_instance, ]
        html = renderit_instance.render_plugin(PluginContext(
            dict={'request': None},
            instance=renderit_instance,
            placeholder=placeholder,
        ))
        self.assertEqual('just some text', html)

    def test_text_plugin_with_url(self):
        placeholder = Placeholder.objects.create()
        renderit_instance = add_plugin(
            placeholder,
            RenderItPlugin,
            'en',
        )
        text_instance = add_plugin(
            placeholder,
            TextPlugin,
            'en',
            body='admin: {% url "admin:index" %}',
        )
        renderit_instance.child_plugin_instances = [text_instance, ]
        html = renderit_instance.render_plugin(PluginContext(
            dict={'request': None},
            instance=renderit_instance,
            placeholder=placeholder,
        ))
        self.assertEqual('admin: /en/admin/', html)

    @override_settings(CMS_RENDERIT_TAG_LIBRARIES=('sample_tags', ))
    def test_text_plugin_with_custom_tag(self):
        placeholder = Placeholder.objects.create()
        renderit_instance = add_plugin(
            placeholder,
            RenderItPlugin,
            'en',
        )
        text_instance = add_plugin(
            placeholder,
            TextPlugin,
            'en',
            body='sample: {% sample %}',
        )
        renderit_instance.child_plugin_instances = [text_instance, ]
        html = renderit_instance.render_plugin(PluginContext(
            dict={'request': None},
            instance=renderit_instance,
            placeholder=placeholder,
        ))
        self.assertIn('HERE BE DA SIMPLE TAG!', html)
