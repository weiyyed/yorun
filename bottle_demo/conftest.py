import pytest
import sys
import requests

@pytest.fixture()
def conf(request):
    # request.config.getini(name='url')
    request.config.getoption('url')

