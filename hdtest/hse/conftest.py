# -*- coding: utf-8 -*-
import pytest

@pytest.fixture(scope="class")
def session(login_hse):
    """sy登录的session"""
    return login_hse

