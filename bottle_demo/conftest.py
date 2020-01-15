import pytest
import sys
import requests

def pytest_collect_file(path, parent):
    """
    定义yml后缀, 且以unit开头的文件, 将被诹
    :param path: 文件全路径
    :param parent: session
    :return: collector
    """
    if path.ext == ".yaml" and path.basename.startswith("test"):
        return YamlFile(path, parent)


class YamlFile(pytest.File):

    def collect(self):
        '''
        collector调用collect方法, 会从文件中提取Item对象, 即testcase
        :return: [Items]
        '''
        import yaml
        raw = yaml.safe_load(self.fspath.open())
        for name, attrs in raw.items():
            yield YamlItem(name, self, attrs)

class YamlItem(pytest.Item):
    def __init__(self, name, parent, attrs):
        # super(YamlItem, self).__init__(name, parent)
        super().__init__(name, parent)
        self.attrs = attrs

    def setup(self):
        '''
        Item 对象的初始化步骤, 同样还有teardown方法, 这里省略
        :return:
        '''
        if 'setup' in self.attrs:
            for action, args in self.attrs['setup'].items():
                getattr(sys.modules['builtins'], action)(args)
    def runtest(self):
        '''
        执行Item对象时, 会调用runtest方法
        所以这里定义具体的测试行为
        :return:
        '''
        try:
            url = self.attrs['body']['url']
            data = self.attrs['body']['data']
            expected = self.attrs['expected']

            resp = requests.get(url, params=data)
            actual = resp.json()

            for key, value in expected.items():
                assert actual['args'][key] == value
        except KeyError:
            raise YamlException(self.name)

    def repr_failure(self, excinfo):
        """ called when self.runtest() raises an exception. """
        if isinstance(excinfo.value, YamlException):
            return "\n".join(
                [
                    "usecase execution failed",
                    "   spec failed: {1!r}: {2!r}".format(*excinfo.value.args),
                    "   no further details known at this point.",
                ]
            )

    def reportinfo(self):
        return self.fspath, 0, "usecase: {}".format(self.name)
class YamlException(Exception):
    pass