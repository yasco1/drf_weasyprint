# DRF WEASYPRINT

A Django REST Framework package for generating and serving PDF files in your web applications using weasyprint.

## Features

- Generate PDF files dynamically.
- Serve PDFs as API responses.
- Customizable templates for PDF generation.

## Installation

```bash
pip install drf-weasyprint
```

## Prerequisites

Before using this package, ensure you have WeasyPrint installed. You can install it using pip:

```bash
pip install weasyprint
```

For detailed installation instructions and additional dependencies, refer to the [WeasyPrint installation guide](https://doc.courtbouillon.org/weasyprint/stable/index.html).

## Usage

1. Configure weasyprint font:

    ```python
    # In settings.py file

    DRF_WEASYPRINT = {
        "DEFAULT_WEASYPRINT_FONT_CONFIG": "path.to.your.CustomFontConfiguration", # DEFAULT "weasyprint.text.fonts.FontConfiguration"
        "WEASYPRINT_LOG_PATH": "path/to/your/logfile",# DEFAULT None
        "DATA_CONTEXT_NAME": "data", # DEFAULT "data"
    }
    ```

2. Create a view to generate and serve PDFs:

    ```python
    from rest_framework.generics import GenericAPIView
    from drf_weasyprint.mixins import PDFFileMixin
    from drf_weasyprint.renderers import WeasyPrintPDFRenderer
    

    class MyPDFView(PDFFileMixin, GenericAPIView):
        renderer_classes = [WeasyPrintPDFRenderer]
        template_name = 'my_template.html'
        filename = 'output.pdf'
    ```

3. Add the view to your `urls.py`:

    ```python
    from django.urls import path
    from .views import MyPDFView

    urlpatterns = [
         path('pdf/', MyPDFView.as_view(), name='pdf-view'),
    ]
    ```

4. Create a template (`my_template.html`) for the PDF content.

    For more information on WeasyPrint and its capabilities, visit the [WeasyPrint documentation](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html).

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any bugs or feature requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.