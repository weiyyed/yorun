# -*- coding: utf-8 -*-
import pytest
from hdtest.conftest import HSE_META_URLS

class TestSy:
    @pytest.mark.parametrize("url",HSE_META_URLS,ids=HSE_META_URLS)
    def test_meta(self,session,url):
        r=session.get(url)
        assert r.status_code==200


if __name__ == '__main__':
    pytest.main()