# -*- coding:utf-8 -*-

import sys
import os
import re

from robot.api import logger
from HttpLibrary import HTTP

from ExtendExcelLibrary import ExtendExcelLibrary

reload(sys)
sys.setdefaultencoding('utf8')


class ExtendHttpLibrary(HTTP):
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        HTTP.__init__(self)

        self.excel = ExtendExcelLibrary()

        self.request_headers = {}

        self.request_templete = {
            "request_host": "",
            "request_scheme": "",
            "request_url_cookie": "",
            "request_module": "",
            "request_doc": "",
            "request_index": "",
            "request_method": "",
            "request_url": "",
            "request_url_para": "",
            "request_body_type": "",
            "request_body": ""
        }

        self.save_host = None

        self.response_status = ""
        self.response_body = ""

    def _init_request_templete(self):
        for key in self.request_templete.keys():
            self.request_templete[key] = ""

    def _pretty_request(self):
        msg = '''
        *   *  *****  *****  *****
        *   *    *      *    *   *
        *****    *      *    *****
        *   *    *      *    *
        *   *    *      *    *
        '''

        # 请求头
        msg += "\n--- Request_Headers: ---\n"
        for key, value in self.request_headers.items():
            msg += "| " + key + ": " + value + "\n"

        # 请求模板
        msg += "\n--- Request_Info: ---\n"
        msg += "| request_host : " + self.request_templete["request_host"] + "\n"
        msg += "| request_scheme : " + self.request_templete["request_scheme"] + "\n"
        msg += "| request_module : " + self.request_templete["request_module"] + "\n"
        msg += "| request_doc : " + self.request_templete["request_doc"] + "\n"
        msg += "| request_index : " + self.request_templete["request_index"] + "\n"
        msg += "| request_method : " + self.request_templete["request_method"] + "\n"
        msg += "| request_url : " + self.request_templete["request_url"] + "\n"
        msg += "| request_url_cookie : " + self.request_templete["request_url_cookie"] + "\n"
        msg += "| request_url_para : " + self.request_templete["request_url_para"] + "\n"
        msg += "| request_body : " + self.request_templete["request_body"] + "\n"

        logger.info(msg, html=False, also_console=False)

    def _pretty_response(self):
        self.response_status = self.get_response_status()
        self.response_body = self.get_response_body()

        msg = "\n--- Response_Info: ---\n"
        msg += "| response_status : " + self.response_status + "\n"

        # 如果是html格式就不打印
        if "DOCTYPE" in self.response_body:
            msg += "| response_body : html格式" + "\n"
        else:
            msg += "| response_body : " + self.response_body + "\n"

        msg += "\n        * * * * * * * * * *        \n"
        logger.info(msg, html=False, also_console=False)

    def get_request_templete(self, key):
        '''
        keys : request_host、request_scheme、request_url_cookie、request_module、request_doc、request_index、request_method、request_url、request_url_para、request_body_type、request_body
        '''
        if key in self.request_templete.keys():
            return self.request_templete[key]
        else:
            return None

    def set_request_templete(self, key, value):
        '''
        keys : request_host、request_scheme、request_url_cookie、request_module、request_doc、request_index、request_method、request_url、request_url_para、request_body_type、request_body
        '''
        if key in self.request_templete.keys():
            self.request_templete[key] = value

    def add_request_header(self, header_name, header_value):
        self.request_headers[header_name] = header_value

    def create_context(self, host=None, scheme='http', is_repeat='False'):
        '''
        is_repeat为True，每次都会创建链接；为False，则判断上一个host是否和当前host一致，不一致创建链接。
        '''
        if (self.save_host != host) or (is_repeat == 'True'):
            self.save_host = host
            self.create_http_context(host, scheme)

        self.request_templete["request_host"] = self.save_host
        self.request_templete["request_scheme"] = scheme

    def add_url_cookie(self, cookie):
        self.request_templete["request_url_cookie"] = cookie

    def load_interface_templete(self, excel_path, request_index):
        self.excel.open_excel(excel_path.decode('utf-8'))

        excel_name = os.path.basename(excel_path)
        sheet_name = str(excel_name).replace(".xlsx", "")

        request_index_strip = str(request_index).strip()
        find_index = None

        rows = self.excel.get_row_count(sheet_name)
        for row in range(rows):
            cell_data = self.excel.read_cell_data(sheet_name, 0, row)

            if cell_data == request_index_strip:
                logger.info("加载接口模板：%s   %s" % (sheet_name, request_index))
                self.request_templete["request_module"] = sheet_name
                self.request_templete["request_index"] = request_index
                self.request_templete["request_doc"] = self.excel.read_cell_data(sheet_name, 1, row)
                self.request_templete["request_method"] = self.excel.read_cell_data(sheet_name, 2, row)
                self.request_templete["request_url"] = self.excel.read_cell_data(sheet_name, 3, row)
                self.request_templete["request_url_para"] = self.excel.read_cell_data(sheet_name, 4, row)
                self.request_templete["request_body_type"] = self.excel.read_cell_data(sheet_name, 5, row)
                self.request_templete["request_body"] = self.excel.read_cell_data(sheet_name, 6, row)
                self.response_status = self.excel.read_cell_data(sheet_name, 7, row)
                find_index = True
                break

        if find_index is None:
            raise ValueError("找不到接口索引 ： %s" % (request_index_strip))

    def send_request(self):
        logger.info("发送一个接口请求：")
        # 申请请求数据类型
        content_type = self.request_templete["request_body_type"]
        if "application/json" in content_type:
            self.add_request_header("Content-Type", content_type)

        # 设置请求body
        body = self.request_templete["request_body"]
        if body != "":
            self.set_request_body(body)

        # 拼装真实的url
        real_url = ""
        if self.request_templete["request_url_cookie"] != "":
            url = self.request_templete["request_url"] + self.request_templete["request_url_cookie"]
        else:
            url = self.request_templete["request_url"]

        url_para = self.request_templete["request_url_para"]
        if url_para == "":
            real_url = url
        else:
            real_url = url + '?' + url_para

        # 设置请求headers
        if self.request_headers != {}:
            for key, value in self.request_headers.items():
                self.set_request_header(key, value)

        # 打印请求配置
        self._pretty_request()

        # 发送请求
        method = self.request_templete["request_method"]
        if method in ("POST", "GET", "PUT", "DELETE"):
            if method == "POST":
                self.POST(real_url)
            if method == "GET":
                self.GET(real_url)
            if method == "PUT":
                self.PUT(real_url)
            if method == "DELETE":
                self.DELETE(real_url)

            # 打印response
            self._pretty_response()

            # 初始化headers和body
            self.request_headers = {}
            self._init_request_templete()

            return self.response_status, self.response_body
        else:
            logger.info("method is not support:%s" % method)

    def get_json_value_by_path(self, json_pointer):
        '''
        通过xpath获取直接获取上一个请求的响应json的值
        '''
        if self.response_body != "":
            ret_value = self.get_json_value(self.response_body, json_pointer)
            logger.info("获取json格式的响应body：json_pointer---%s" % json_pointer)
            return ret_value

    def set_json_value_by_path(self, json_pointer, json_value):
        '''
        通过xpath设置请求json的值
        '''
        request_body = self.request_templete["request_body"]
        if request_body != "":
            self.request_templete["request_body"] = self.set_json_value(request_body, json_pointer, json_value)
            logger.info("修改json格式的请求body：json_pointer---%s json_value---%s" % (json_pointer, json_value))

    def verify_response_status(self, status):
        '''
        验证响应的状态码
        '''
        if status != "":
            assert self.response_status.find(status) != -1, '响应状态码错误！ does not contain %s.' % status

    def modify_url(self, para, value):
        '''
        参数使用 {} 包裹进行标记，替换时连同 {} 一起替换
        '''
        logger.info("修改url的参数：para---%s value---%s" % (para, value))
        para = "{" + para + "}"
        url = self.request_templete["request_url"]
        self.request_templete["request_url"] = str(url).replace(para, value)

    def modify_url_para(self, para, value):
        '''
        ${para}=(.*?)[&]
        ${para}=${value}&
        '''
        logger.info("修改url_para的参数：para---%s value---%s" % (para, value))
        pattern = str(para) + "=(.*?)[&]"
        repl = str(para) + "=" + str(value) + "&"
        string = self.request_templete["request_url_para"] + "&"
        ret_string = re.sub(pattern, repl, string)
        self.request_templete["request_url_para"] = ret_string[:-1]
