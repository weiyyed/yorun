# -*- coding: utf-8 -*-
import pytest
from hdtest.conftest import session_menu_urls
from urllib.parse import urljoin


class TestSy:
    ids = ["{}/getMetaData".format(url) for s, url in session_menu_urls]
    @pytest.mark.parametrize("session,url",session_menu_urls,ids=ids)
    def test_meta(self,session,url):
        url=urljoin(url,"getMetaData")
        r=session.get(url)
        assert r.status_code==200


if __name__ == '__main__':
    pytest.main()