import os
import pytest
from _pytest.config import Config
import importlib
import  pathlib
# 导入环境的配置文件
conf_file='prod'
exec('from conf.{} import *'.format(conf_file))

if __name__ == '__main__':
    # pytest.main(["--html={}".format(reportfile)])
    pytest.main()
