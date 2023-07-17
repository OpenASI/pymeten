# https://circleci.com/blog/publishing-a-python-package/?utm_source=google&utm_medium=sem&utm_campaign=sem-google-dg--japac-en-dsa-tROAS-auth-nb&utm_term=g_-_c__dsa_&utm_content=&gclid=Cj0KCQjwzdOlBhCNARIsAPMwjbwdmJCEbsBrqMLOreMW3MpwB3Fn_goelbiBY9RaLQ_IeOJKleiSjYMaAuiZEALw_wcB

# python setup.py sdist bdist_wheel
# twine upload --repository testpypi dist/*
# pip install --index-url https://test.pypi.org/simple convsn
