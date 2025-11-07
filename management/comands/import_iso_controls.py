import pandas as pd
from django.core.management.base import BaseCommand
from portal.models import Control, Risk
from pathlib import Path

class Command(BaseCommand):
    help = "Importa controles ISO y riesgos desde /mnt/data/Iso 27001.xlsx"

    def handle(self, *args, **options):
        path = Path('/mnt/data/Iso 27001.xlsx')
        if not path.exists():
            self.stdout.write(self.style.ERROR(f"No existe el archivo: {path}"))
            return

        xls = pd.ExcelFile(path)
        # Intentamos leer hoja 'ISO 27001' y 'Corte 2' como en tu archivo
        try:
            iso_df = xls.parse('ISO 27001')
        except Exception:
            iso_df = xls.parse(xls.sheet_names[0])

        # Se buscan columnas que contengan IDs/títulos/descripciones.
        # Ajusta los nombres de columnas si tu Excel usa otros encabezados.
        candidate_cols = list(iso_df.columns)
        # Heurística: si hay columnas sin nombre o col2/3/4
        def get_val(row, possible_idxs):
            for i in possible_idxs:
                if i < len(row):
                    v = row[i]
                    if pd.notna(v):
                        return str(v).strip()
            return ''

        Control.objects.all().delete()
        imported = 0
        for _, row in iso_df.iterrows():
            # heurística: tomar la tercera, cuarta y quinta columna si existen
            control_id = get_val(row.tolist(), [2,0,1])
            title = get_val(row.tolist(), [3,1,2])
            description = get_val(row.tolist(), [4,5,6])
            if control_id and title:
                Control.objects.create(control_id=control_id, title=title, description=description)
                imported += 1

        # Riesgos desde 'Corte 2' hoja (si existe)
        risks_imported = 0
        if 'Corte 2' in xls.sheet_names:
            corte_df = xls.parse('Corte 2')
            # heurística: buscar una celda con texto grande que contenga comas entre riesgos
            text = ''
            # buscar primeras filas con texto
            for col in corte_df.columns:
                sample = corte_df[col].dropna().astype(str).head(10).tolist()
                if sample:
                    text = ' '.join(sample)
                    if len(text) > 30:
                        break
            if text:
                # extraer items separados por comas o saltos de linea
                parts = [p.strip() for p in (text.replace('\n',',')).split(',') if p.strip()]
                Risk.objects.all().delete()
                for p in parts[:100]:
                    Risk.objects.create(name=p)
                    risks_imported += 1

        self.stdout.write(self.style.SUCCESS(f"Controles importados: {imported}"))
        self.stdout.write(self.style.SUCCESS(f"Riesgos importados: {risks_imported}"))
