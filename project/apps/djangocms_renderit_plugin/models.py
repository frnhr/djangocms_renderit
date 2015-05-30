from django.db import models
from cms.models import CMSPlugin


class RenderitCMSPlugin(CMSPlugin):
    tag_libraries = models.CharField(max_length=255, null=False, blank=True, default='',
                                     help_text='Custom tag libraries, space-separated')

    def render_plugin(self, context=None, placeholder=None, admin=False, processors=None):
        try:
            output = super().render_plugin(context, placeholder, admin, processors)
        except Exception as e:
            return "error: {}".format(e)
            raise e
        return output
