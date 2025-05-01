from django.utils.encoding import escape_uri_path
from rest_framework.response import Response


class PDFFileMixin(object):
    """
    Mixin to provide PDF export functionality with customizable filenames.
    """

    filename = "export.pdf"

    def get_filename(self, request=None, *args, **kwargs):
        """
        Get the filename for the PDF export.

        This method can be overridden in subclasses to customize the filename.

        Args:
            request (HttpRequest, optional): The current request. Defaults to None.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The filename for the PDF export.
        """
        return self.filename

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Customize the response to include the correct content disposition header
        for PDF files, allowing the client to download the file with a meaningful name.

        Args:
            request (HttpRequest): The current request.
            response (Response): The response object to finalize.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The finalized response object.
        """
        response = super().finalize_response(request, response, *args, **kwargs)

        if isinstance(response, Response) and getattr(response.accepted_renderer, "format", None) == "pdf":
            filename = self.get_filename(request=request, *args, **kwargs)
            response["Content-Disposition"] = f"inline; filename={escape_uri_path(filename)}"

        return response
