from setuptools import setup, find_packages

setup(
    name='drf_weasyprint',
    version='1.0.0',
    packages=find_packages(),
    author='Mohamed Yassin (yasco1)',
    author_email='muhamad_yassin@hotmail.com',
    description='A Django REST Framework package for generating PDF files with WeasyPrint.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yasco1/drf_weasyprint',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.9',
    install_requires=[
        'djangorestframework>=3.14.0',
        'weasyprint>=65.1'
    ],
)
