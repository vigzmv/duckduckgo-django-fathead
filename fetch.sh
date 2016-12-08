#!/bin/bash

mkdir -p download
cd download
rm -f *.html
wget --quiet https://docs.djangoproject.com/en/1.10/ref/templates/builtins/ -O index.html
# https://docs.djangoproject.com/en/1.10/ref/settings/
# https://docs.djangoproject.com/en/1.10/ref/utils/
# https://docs.djangoproject.com/en/1.10/ref/validators/
# https://docs.djangoproject.com/en/1.10/ref/views/
# https://docs.djangoproject.com/en/1.10/ref/urlresolvers/
# https://docs.djangoproject.com/en/1.10/ref/urls/
# https://docs.djangoproject.com/en/1.10/ref/models/database-functions/
# https://docs.djangoproject.com/en/1.10/ref/models/fields/
# https://docs.djangoproject.com/en/1.10/ref/forms/api/
# https://docs.djangoproject.com/en/1.10/ref/forms/fields/
# https://docs.djangoproject.com/en/1.10/ref/forms/widgets/
# https://docs.djangoproject.com/en/1.10/ref/migration-operations/
# https://docs.djangoproject.com/en/1.10/ref/contrib/
# https://docs.djangoproject.com/en/1.10/ref/django-admin/
