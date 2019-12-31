# -*- coding: utf-8 -*-
import pytest

@pytest.fixture(scope="class")
def session(login_eam):
    """sy登录的session"""
    return login_eam

