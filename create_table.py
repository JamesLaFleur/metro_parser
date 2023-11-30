import xlsxwriter
import os
from main import parseData, URL

NAMES = ['Артикул', 'Название', 'Новая цена', 'Старая цена', 'Бренд', 'Ссылка']

def writer(parser):
    path = os.path.join(os.getcwd(), 'data.xlsx')

    if os.path.isfile(path):
        os.remove(path)

    book = xlsxwriter.Workbook(path)
    page = book.add_worksheet("Product")
    bold = book.add_format({'bold': True})

    row = 1
    column = 0

    page.set_column("A:A", 20)
    page.set_column("B:B", 20)
    page.set_column("C:C", 50)
    page.set_column("D:D", 50)
    page.set_column("E:E", 50)
    page.set_column("F:F", 50)

    title_column = 0
    for name in NAMES:
        page.write(0, title_column, name, bold)
        title_column += 1


    for items in parser(URL):
        for item in items:
            page.write(row, column, item.get('ProductID'))
            page.write(row, column+1, item.get('Product_name'))
            page.write(row, column+2, item.get('Actual_price'))
            page.write(row, column+3, item.get('Old_price'))
            page.write(row, column+4, item.get('Brand'))
            page.write(row, column+5, item.get('Product_link'))
            row += 1

    book.close()


writer(parseData)