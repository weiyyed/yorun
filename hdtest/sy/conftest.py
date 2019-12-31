# -*- coding: utf-8 -*-
import pytest

@pytest.fixture(scope="class")
def session(login_sy):
    """sy登录的session"""
    return login_sy

