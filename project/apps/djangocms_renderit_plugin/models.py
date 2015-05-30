from django.db import models
from django.conf import settings
from cms.models import CMSPlugin
from django.template import Template


TEMPLATE = (
    '{% load cms_tags #ADDITIONAL_LIBRARIES# %}'
    '#OUTPUT#')


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


def render_exception(e, output=None):
    return ERROR_TEMPLATE.format(
        message=str(e),
        output_html='' if not output else ERROR_OUTPUT_TEMPLATE.format(output),
    )


class RenderitCMSPlugin(CMSPlugin):
    tag_libraries = models.CharField(max_length=255, null=False, blank=True, default='',
                                     help_text='Custom tag libraries, space-separated')

    def _get_tag_libraries(self):
        try:
            libraries = ' '.join(map(str, settings.CMS_RENDERIT_TAG_LIBRARIES))
        except AttributeError:
            libraries = ''
        if self.tag_libraries:
            libraries = ' '.join((libraries, self.tag_libraries))
        return libraries

    def render_plugin(self, context=None, placeholder=None, admin=False, processors=None):
        output = super().render_plugin(context, placeholder, admin, processors)

        template_str = TEMPLATE.replace(
            '#OUTPUT#', output
        ).replace(
            '#ADDITIONAL_LIBRARIES#', self._get_tag_libraries()
        )
        try:
            return Template(template_str).render(context)
        except Exception as e:
            return render_exception(e, output)
