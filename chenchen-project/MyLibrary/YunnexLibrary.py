# -*- coding:utf-8 -*-

import sys
import re
import qrcode
from robot.libraries.XML import XML
from robot.api import logger

reload(sys)
sys.setdefaultencoding('utf8')


class YunnexLibrary:
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        self.xml_obj = XML()

    def generate_qrcode_img(self, href, generate_img_path):
        """Generating a qr code from URL.
        e.g., generate_qrcode_img("www.baidu.com", "C:/1.png")
        """
        img = qrcode.make(href)
        img.save(generate_img_path)

    def get_table_from_html(self, html, index):
        '''
        从html中截取表格tbody，index从0开始
        '''
        if "<tbody>" in html:
            # 去除换行和空白
            html = html.replace("\n", "")
            html = html.replace("\r", "")
            html = html.replace("\t", "")
            html = re.sub(">\s+<", "><", html)

            # 截取
            tbodys = re.findall(r"<tbody>(.*?)</tbody>", html)
            logger.info("从html中截取表格tbodys：%s" % tbodys)
            tbody = "<tbody>" + tbodys[int(index)] + "</tbody>"
            logger.info("index = %s ; tbody = %s" % (index, tbody))

            return tbody
        else:
            logger.info("Not found tbody")
            return None

    def verify_tbody(self, tbody, row, *para):
        '''
        验证表格内容，入参为“-”则不验证
        '''
        logger.info("验证表格第%s行数据：表格数据 == 验证数据" % row)

        # 把异常节点去除掉<br><br \>，替换成空格
        tbody = re.sub("<br \\\>|<br>", " ", tbody)

        xml = self.xml_obj.parse_xml(tbody)
        cols = len(para)

        for col in range(1, int(cols) + 1):
            if para[int(col) - 1] != "-":
                xpath = "tr[%s]/td[%s]" % (row, col)
                cell_text = self.xml_obj.get_element_text(xml, xpath)
                logger.info("第%s列数据：   %s == %s" % (col, str(cell_text).strip(), str(para[int(col) - 1])))
                assert str(cell_text).strip() == str(para[int(col) - 1])

    def get_table_value_by_xpath(self, tbody, xpath):
        '''
        通过xpath获取表格内容,xpath从第二个节点开始写，eg. tr[1]/td[2]
        '''
        logger.info("通过xpath获取表格数据，xpath = %s" % xpath)

        # 把异常节点去除掉<br><br \>，替换成空格
        tbody = re.sub("<br \\\>|<br>", " ", tbody)

        xml = self.xml_obj.parse_xml(tbody)
        cell_text = self.xml_obj.get_element_text(xml, xpath)
        return cell_text.strip()


if __name__ == "__main__":
    s = '''
    '''
    yunnexlibrary = YunnexLibrary()
    print yunnexlibrary.get_table_value_by_xpath(s, "div[2]/div[1]/a/p[1]")
