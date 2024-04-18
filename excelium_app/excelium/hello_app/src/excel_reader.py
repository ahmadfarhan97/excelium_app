import pandas as pd


class ReadFile:
    def __init__(self, data: object) -> None:
        self.data = data

    def excel_file(self):
        data = self.data
        xls = pd.ExcelFile(data)
        return xls

    def read_xlsx(self):
        xls = self.excel_file()
        read_xls = pd.read_excel(xls)
        return read_xls

    def column_list(self):
        xlsx = self.read_xlsx()
        columns_list = xlsx.columns
        return columns_list

    def tabs_list(self):
        xls = self.excel_file()
        sheet_names = xls.sheet_names
        if not len(sheet_names):
            print(len(sheet_names))
        else:
            print(sheet_names)
            return sheet_names

    def read_tabs_xlsx(self, sheet):
        # xls = pd.ExcelFile(self.data)
        read_xls = pd.read_excel(self.data, sheet_name=sheet)
        return read_xls

    def tab_column_list(self, sheet):
        xlsx = self.read_tabs_xlsx(sheet)
        tab_column_list = xlsx.columns
        return tab_column_list
