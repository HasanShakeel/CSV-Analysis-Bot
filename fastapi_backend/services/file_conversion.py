import pandas as pd
import os

def convert_excel_to_csv(xlsx_filename):
    try:
        # Specify the engine manually (e.g., 'openpyxl' for .xlsx files)
        if xlsx_filename.endswith('.xlsx'):
            engine = 'openpyxl'
        elif xlsx_filename.endswith('.xls'):
            engine = 'xlrd'
        else:
            raise ValueError("Unsupported file format")

        xls = pd.ExcelFile(xlsx_filename, engine=engine)
        sheet_names = xls.sheet_names
        
        for sheet_name in sheet_names:
            if sheet_name.lower() == 'results':
                csv_filename = 'results.csv'
            elif sheet_name.lower() == 'targets':
                csv_filename = 'targets.csv'
            else:
                csv_filename = f"{os.path.splitext(xlsx_filename)[0]}_{sheet_name}.csv"
                
            df = pd.read_excel(xlsx_filename, sheet_name=sheet_name, engine=engine)
            df.to_csv(csv_filename, index=False)
            print(f"Sheet '{sheet_name}' converted to {csv_filename}")
    
    except Exception as e:
        raise Exception(f"Error converting Excel to CSV: {e}")
