from django.db import models
from cms.models import CMSPlugin


class RenderitCMSPlugin(CMSPlugin):

    def render_plugin(self, context=None, placeholder=None, admin=False, processors=None):
        try:
            output = super().render_plugin(context, placeholder, admin, processors)
        except Exception as e:
            return "error: {}".format(e)
            raise e
        return output
