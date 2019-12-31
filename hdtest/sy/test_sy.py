# -*- coding: utf-8 -*-
import pytest

from hdtest.conftest import SY_META_URLS


class TestSy:
    @pytest.mark.parametrize("url",SY_META_URLS,ids=SY_META_URLS)
    def test_meta(self,session,url):
        r=session.get(url)
        assert r.status_code==200


if __name__ == '__main__':
    pytest.main()