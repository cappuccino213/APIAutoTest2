"""
@File : conftest.py
@Date : 2023/4/4 15:44
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import pytest

"""用于写hook函数或全局的fixture"""


# 自定义变量的注册
def pytest_addoption(parser):
	parser.addini("test_host", default="http://192.168.1.18", help="请在pytest.ini配置正确的测试host")
	parser.addini("host", default="http://192.168.1.56", help="请在pytest.ini配置正式host")
	parser.addini("test_port", default="80", help="请在pytest.ini配置正确的测试port")
	parser.addini("port", default="80", help="请在pytest.ini配置正式的port")


# 读取自定义的变量
@pytest.fixture()
def args_ini(pytestconfig):
	return dict(test_host=pytestconfig.getini("test_host"),
	            test_port=pytestconfig.getini("test_port"),
	            host=pytestconfig.getini("host"),
	            port=pytestconfig.getini("port"))


if __name__ == "__main__":
	pass
