from tempfile import NamedTemporaryFile
from typing import List, Dict
from openpyxl import Workbook


class ExportService:

    @staticmethod
    def export_rows_to_excel(rows: List[Dict[str, str]],
                             filename: str = 'results.xlsx') -> str:
        wb = Workbook()
        ws = wb.active
        ws.title = 'results'
        ws.append(['变量', '结果'])
        for row in rows:
            ws.append([row.get('var', ''), row.get('result', '')])

        tmp = NamedTemporaryFile(delete=False, suffix='.xlsx')
        wb.save(tmp.name)
        tmp.flush()
        return tmp.name
