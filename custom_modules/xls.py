import xlrd
import os


class XlsTools:
    """
    Helper for finding values in an xls document
    https://blogs.harvard.edu/rprasad/2014/06/16/reading-excel-with-python-xlrd/
    """
    def __init__(self, filename, sheet_name='', sheet_index=0):
        if not os.path.isfile(filename):
            raise FileNotFoundError('Can\'t find file: ' + filename)
        else:
            if not os.access(filename, os.R_OK):
                raise PermissionError('Can\'t access file: ' + filename)
        self.xl_workbook = xlrd.open_workbook(filename)
        self.xl_sheet = self.xl_workbook.sheet_by_name(sheet_name) if sheet_name \
            else self.xl_workbook.sheet_by_index(sheet_index)

    def find(self, find_value, x_offset=0, y_offset=0):
        for row_no in range(0, self.xl_sheet.nrows):
            for column_no in range(0, self.xl_sheet.ncols):
                if self.xl_sheet.cell(row_no, column_no).value == find_value:
                    return_string = self.xl_sheet.cell(row_no + y_offset, column_no + x_offset).value
                    return return_string if return_string is not None else ''
