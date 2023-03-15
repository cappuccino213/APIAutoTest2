"""
@File : http_base.py
@Date : 2023/3/14 10:16
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import json
import logging

import pytest
import requests

from data_source import DataSource


class TestHttpBase:
	logger = logging.getLogger(__name__)
	logging.basicConfig(level=logging.INFO)
	
	ds = DataSource('./test_case/case_data.xlsx')
	# ds = DataSource('../test_case/case_data.xlsx')  在当前代码执行用这个目录
	
	header = {'Content-Type': 'application/json'}
	
	test_result = []
	
	# 每次方法执行前执行
	def setup_method(self):
		self.logger.info("执行前准备...")
	
	# 每次方法执行后执行
	def teardown_method(self):
		pass
	
	# 授权函数
	def get_token(self):
		return requests.post(url="http://192.168.1.18:8709/Token/RetriveInternal",
		                     json=dict(ProductName='eWordRIS', HospitalCode='QWYHZYFZX',
		                               RequestIP='192.168.1.56'),
		                     headers=self.header).json()['token']
	
	# 执行脚本
	@pytest.mark.parametrize('data', ds.data_source)
	def test_request_base(self, data):
		url = data['host'] + data['api']
		payload = data['body']
		params = data['params']
		# 取头信息，如果测试数据中有则取数据中的，无则用默认值
		if data['headers']:
			self.header = json.loads(data['headers'])
		self.header['Authorization'] = self.get_token()
		try:
			# 获取结果数据
			res = requests.request(method=data['method'], url=url, headers=self.header, params=params, data=payload,
			                       timeout=5)
			res_code = res.status_code
			res_json = res.json()
			# 将测试数据与结果数据合并
			self.test_result.append(
				data | {'actual_code': res_code, 'result': str(res_json),
				        'rt(ms)': round(res.elapsed.total_seconds() * 1000)})
			assert float(res_code) == float(data['expect_code'])
		except requests.RequestException as e:
			res_code = 500
			res_json = {'exception': str(e)}
			self.test_result.append(data | {'actual_code': res_code, 'result': str(res_json), 'rt(ms)': '--'})
			assert float(res_code) == float(data['expect_code'])
	
	# 所有方法测试脚本执行完执行
	def teardown_class(self):
		logging.info(self.test_result)
		# 将测试结果填入表格
		self.ds.write_data(self.test_result)


if __name__ == "__main__":
	pytest.main(['-v'])
