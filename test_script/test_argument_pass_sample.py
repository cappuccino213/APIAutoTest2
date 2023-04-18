"""
@File : test_argument_pass_sample.py
@Date : 2023/4/18 15:09
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import logging
import requests

import pytest


# @pytest.mark.show_data
class TestShowData:
	logger = logging.getLogger(__name__)
	logging.basicConfig(level=logging.INFO)
	
	# 登录账号获取token
	@pytest.fixture()
	def login(self, args_ini):
		result = requests.post(url=f"{args_ini['test_host']}:{args_ini['test_port']}/api/Authorize/Validata",
		                       json={
			                       "AccountName": "admin",
			                       "UserPassWord": "E10ADC3949BA59ABBE56E057F20F883E",
			                       "UseScenario": ""
		                       }, headers={'Content-Type': 'application/json'})
		return result.json()["token"]
	
	# 获取token值
	def test_show_data(self, args_ini, login, run_function):
		url = f"{args_ini['test_host']}:{args_ini['test_port']}/api/DataScreenInfo/Show"
		payload = {"permissionCode": "RadiologyDataScreen_1", "data": ""}
		header = {'Content-Type': 'application/json',
		          'Authorization': login}
		res = requests.post(url=url, json=payload, headers=header, timeout=5)
		self.logger.info(res.json())
		assert res.json()["isSuccess"]
	
	# 前置后置，yield语句之前的在测试用例之前，之后的语句就会在测试用例执行完成之后再执行。
	@pytest.fixture()
	def run_function(self):
		print("开始接口测试...")
		yield
		print("结束接口测试...")


# print(res.json())


if __name__ == "__main__":
	pass
