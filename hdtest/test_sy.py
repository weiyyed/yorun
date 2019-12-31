# -*- coding: utf-8 -*-
import requests,pytest
@pytest.mark.usefixtures("login_session",scope="class")
class Sy:
    def test_org(self):
        r=login_session.get("http://sy.51gxc.com/sy/SY_USER/getMetaData?0.39052259724308946&contentType=json&ajax=true&tid=2000000000704")
        assert r.state_code==200
