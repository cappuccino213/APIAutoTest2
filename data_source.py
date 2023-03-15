"""
@File : data_source.py
@Date : 2023/3/14 10:48
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import xlrd
import xlwt
import logging
import os

from datetime import datetime


class DataSource:
	logger = logging.getLogger(__name__)
	logging.basicConfig(level=logging.INFO)
	
	def __init__(self, file_path):
		self.data_file = file_path
		self.data_source = self.read_data()
	
	def read_data(self):
		if self.data_file.endswith('xlsx'):
			with xlrd.open_workbook(self.data_file) as book:
				sheet = book.sheet_by_index(0)  # 获取第一个sheet的数据
				data = []
				for row in range(1, sheet.nrows):
					# 获取每行数据
					value_list = sheet.row_values(row)
					# 去除字符串中的空格和换行符
					for col in range(sheet.ncols):
						value_list[col] = str(value_list[col]).replace("\n", "").replace(" ", "")
					data.append(dict(zip(sheet.row_values(0), value_list)))
				self.logger.info(f"获得测试数据{data}")
				return data
		elif self.data_file.endswith('json'):
			pass
		elif self.data_file.endswith('yml'):
			pass
		else:
			self.logger.error("数据源文件格式不正确")
	
	# 写数据到excel
	def write_data(self, data: list[dict]):
		file_path, file_ext = os.path.splitext(self.data_file)
		file_name = file_path + '_result' + file_ext
		wb = xlwt.Workbook()
		sheet = wb.add_sheet(datetime.now().strftime('%Y%m%d%H%M%S'), cell_overwrite_ok=True)
		# 写入标题
		titles = list(data[0].keys())
		for i in range(len(titles)):
			sheet.write(0, i, titles[i])
		# 写入数据
		items = [list(item.values()) for item in data]
		for j in range(len(items)):
			for n in range(len(items[j])):
				sheet.write(j + 1, n, items[j][n])
		wb.save(file_name)


if __name__ == "__main__":
	ds = DataSource('./test_case/case_data.xlsx')
	results = [{'result': 'pass', 'rt': 20}, {'result': 'pass', 'rt': 18}, {'result': 'fail', 'rt': 25}]
	ds.write_data(results)
