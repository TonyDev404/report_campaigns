from typing import List, Dict, Any, cast
from io import BytesIO

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet


class ExcelExporter:
    HEADERS = [
        "brand",
        "channel",
        "campaign",
        "user",
        "attention_level",
    ]
    
    @staticmethod
    def export(rows: List[Dict[str, Any]]) -> BytesIO:
        """
        Genera un archivo Excel en memoria a partir de filas normalizadas.
        """
        wb = Workbook()
        ws = cast(Worksheet, wb.active)
        ws.title = "Campaign Report"
        
        ExcelExporter._write_header(ws)
        ExcelExporter._write_rows(ws, rows)
        
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        return output
        
    @staticmethod
    def _write_header(ws: Worksheet) -> None:
        ws.append(ExcelExporter.HEADERS)
        
    @staticmethod
    def _write_rows(
        ws: Worksheet,
        rows: List[Dict[str, Any]]
    ) -> None:
        for row in rows:
            ws.append([
                row.get("brand"),
                row.get("channel"),
                row.get("campaign"),
                row.get("user"),
                row.get("attention_level"),
            ])