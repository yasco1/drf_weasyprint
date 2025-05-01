import logging
from tempfile import TemporaryFile

from django.template.loader import render_to_string
from rest_framework.renderers import BaseRenderer
from weasyprint import HTML
from drf_weasyprint.settings import api_settings

if api_settings.WEASYPRINT_LOG_PATH is not None:
    logger = logging.getLogger("weasyprint")
    logger.addHandler(logging.FileHandler(api_settings.WEASYPRINT_LOG_PATH))


class WeasyPrintPDFRenderer(BaseRenderer):
    """
    A custom renderer to generate and render PDF responses for Django views.

    This renderer uses a specified template and context data from the associated view
    to generate a PDF document using WeasyPrint.

    Attributes:
        media_type (str): The media type of the renderer. Default is "application/pdf".
        format (str): The format used by the renderer. Default is "pdf".
    """

    media_type = "application/pdf"
    format = "pdf"

    def get_template_name(self, view):
        """
        Retrieves the template name from the view.

        This method first checks for a `template_name` attribute or a `get_template_name` method
        on the view to determine the template to use for rendering.

        Args:
            view (object): The view instance containing template information.

        Returns:
            str: The name of the template to be used.

        Raises:
            AssertionError: If no template name is found on the view.
        """

        template_name = getattr(view, "template_name", None)

        if template_name is None and hasattr(view, "get_template_name"):
            template_name = view.get_template_name()

        if not template_name:
            raise AttributeError(
                "The view must have a template_name attribute or implement get_template_name()."
            )

        return template_name

    def get_context_data(self, view, request):
        """
        Retrieves the context data for the template from the view.

        This method checks for a `template_context` attribute or a `get_template_context` method
        on the view to construct the template context.

        Args:
            view (object): The view instance containing context information.
            request (HttpRequest): The current HTTP request object.

        Returns:
            dict: The context data to be passed to the template.

        Raises:
            AssertionError: If no context data is found on the view.
        """

        context = getattr(view, "template_context", None)

        if context is None and hasattr(view, "get_template_context"):
            context = view.get_template_context(request)

        if context is None:
            return {}

        return context

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders the PDF response using the specified template and context.

        This method generates an HTML string from the template and context data,
        then converts it to a PDF using WeasyPrint.

        Args:
            data (dict): The data to be rendered in the PDF.
            accepted_media_type (str, optional): The accepted media type. Default is None.
            renderer_context (dict, optional): The renderer context containing request and view information. Default is None.

        Returns:
            bytes: The generated PDF content as a byte stream.
        """

        request = renderer_context["request"]
        view = renderer_context["view"]

        # Get the template name and context data from the view
        template_name = self.get_template_name(view)
        context = self.get_context_data(view, request)

        context_name = api_settings.DATA_CONTEXT_NAME
        context.update({context_name: data})

        FONTCONFIG = api_settings.DEFAULT_WEASYPRINT_FONT_CONFIG
        html = render_to_string(
            template_name=template_name, context=context, request=request
        ).encode(encoding="UTF-8")
        document = HTML(string=html, base_url=request.build_absolute_uri()).render(
            font_config=FONTCONFIG()
        )

        return self._save_virtual_pdf(document)

    def _save_virtual_pdf(self, document: HTML):
        """
        Generates a PDF file in memory and returns its content.

        This method uses a temporary file to save the PDF, then reads its content into memory.

        Args:
            document (HTML): The WeasyPrint HTML document to render as PDF.

        Returns:
            bytes: The content of the rendered PDF as a byte stream.
        """

        with TemporaryFile() as tmp:
            document.write_pdf(tmp, optimize_images=False)
            tmp.seek(0)
            return tmp.read()
