# coding=utf-8

import os
import sys

import xlrd

reload(sys)
sys.setdefaultencoding('utf8')


class ExtendExcelLibrary():
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        self.excel = []
        self.data = None

    def _save_excel(self, excel_path):

        excel_dict = {"name": "", "data": ""}
        data = xlrd.open_workbook(filename=excel_path)

        # 只保存文件名和data
        excel_name = os.path.basename(excel_path)
        excel_dict["name"] = excel_name
        excel_dict["data"] = data

        return excel_dict

    def open_excel(self, excel_path):
        """同一个Excel只打开一次
        """
        excel_name = os.path.basename(excel_path)

        # 判断文件是否已经保存
        if excel_name.encode('unicode_escape') not in str(self.excel):
            excel_dict = self._save_excel(excel_path)
            self.excel.append(excel_dict)

        for i in range(len(self.excel)):
            if self.excel[i]["name"] == excel_name:
                self.data = self.excel[i]["data"]
                break

    def read_cell_data(self, sheet_name, column, row):
        """sheet_name, column, row
        """
        table = self.data.sheet_by_name(sheet_name)
        cell_data = table.cell(int(row), int(column)).value

        return cell_data

    def get_row_count(self, sheet_name):
        """sheet_name
        """
        table = self.data.sheet_by_name(sheet_name)
        rows = table.nrows

        return rows
