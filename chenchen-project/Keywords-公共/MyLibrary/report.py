# -*- coding:utf-8 -*-
# _author_ = 'phoebe'
# -*- encoding = cp936 -*-
# Author: Allan
# Version: 2.0
# Data: 2017-5-9
import os, sys
import csv
import xlwt
import datetime


class report():
    def __init__(self):
        #Current Log Path:
        self.curr_dir = 'F:\chenchen-project\Testcase'

    def Read_From_File(self, filename):
        # Read data from the given file
        file = os.path.join(self.curr_dir, filename) # Default File Path
        try:
            f = open(file)
            data = f.read()
        except Exception, e:
            print str(e)
        finally:
            f.close()

        return data

    def Write_To_CSV_File(self, filename, *data):
        """
        Write the values to the CSV file.

        """
        reload(sys)
        sys.setdefaultencoding('cp936')

        with open(filename, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel')
            spamwriter.writerow(['Test Result'])
            spamwriter.writerow(['Case', 'Status', 'Error Message'])
            for row in data:
                for col in row:
                    print col
                    spamwriter.writerow(col)

    def Reorganize_Data(self, data):
        # Reorganize data for writing them to CSV file
        allList = []
        reorganized = data.split('|')
        for row in reorganized:
            allList.append(row.split(':'))
        return allList

    def Set_Style(self, name, height, colour=1, bold=False, pattern_colour=None):
        # default font style

        # Cell set alignment
        alignment = xlwt.Alignment()
        alignment.HORZ = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER

        # Cell add borders
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        borders.left_colour = 0x40
        borders.right_colour = 0x40
        borders.top_colour = 0x40
        borders.bottom_colour = 0x40

        # Cell set font style
        font = xlwt.Font()
        font.name = name
        font.height = height
        font.colour_index = colour
        font.bold = bold

        if pattern_colour != None:
            # Cell set background colour
            pattern = xlwt.Pattern()
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN
            pattern.pattern_fore_colour = pattern_colour

        style = xlwt.XFStyle()
        style.alignment = alignment
        if pattern_colour != None:
            # Cell set background colour
            style.pattern = pattern
        style.borders = borders
        style.font = font
        return style

    def Write_To_Excel_File(self, filename, *data):
        """
        Write the values to the Excel file.

        """
        reload(sys)
        sys.setdefaultencoding('cp936')

        try:
            xls_file = xlwt.Workbook()
            sheet1 = xls_file.add_sheet('Test Report', cell_overwrite_ok=True)

            # Cell set width of column
            col_wid = sheet1.col(0)
            col_wid.width = 256*60
            col_wid = sheet1.col(1)
            col_wid.width = 256*10
            col_wid = sheet1.col(2)
            col_wid.width = 256*60

            # Write report name & subtitle
            started_time = os.getenv('U_CUSTOM_TEST_TASK_START_TIME')
            generated_time = datetime.datetime.now()
            report_status = ['Start Time', '%s' % started_time, 'End Time', '%s' % str(generated_time)]
            row_status = ['Case', 'Status', 'Error Message']
            sheet1.write_merge(0, 3, 0, 0, 'Test Result', self.Set_Style('Arial', 210, 17, True))
            sheet1.write_merge(0, 3, 1, 1, '', self.Set_Style('Arial', 210, 1, True))
            for i in xrange(0, len(report_status)):
                sheet1.write(i, 2, report_status[i], self.Set_Style('Arial', 200, 63))#写入数据在第i行第2列(从0开始计算)

            for i in xrange(0, len(row_status)):
                sheet1.write(4, i, row_status[i], self.Set_Style('Arial', 200, 64, True, pattern_colour=22))

            # Write test result
            for value in data:
                for row in xrange(0, len(value)):
                    print value[row]
                    for col in xrange(len(value[row])):
                        sheet1.write(row+5, col, value[row][col], self.Set_Style('Arial', 200, 64))
        except IOError, e:
            print str(e)
        finally:
            xls_file.save(filename)

    def Create_CSV_Report(self, filename):
        # Create CSV Report | ${filename}
        file = os.path.join(self.curr_dir, 'report.csv') # Default File Path
        lines = self.Read_From_File(filename)
        data = self.Reorganize_Data(lines)
        self.Write_To_CSV_File(file, data)

    def Create_Excel_Report(self, filename):
        # Create Excel Report | ${filename}
        file = os.path.join(self.curr_dir, 'report.xls')
        # Default File Path
        lines = self.Read_From_File(filename)
        data = self.Reorganize_Data(lines)
        self.Write_To_Excel_File(file, data)

if __name__ == '__main__':
    report = report()
    report.Create_Excel_Report('Total_Result.log')
