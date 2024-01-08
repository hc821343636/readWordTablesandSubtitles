import pandas as pd
# 将excel的每一个sheet作为单个csv进行输出到当前文件夹 命名为以前sheet的名字
def save_excel_sheets_as_csv(excel_file_path):
    # Load the Excel file
    xls = pd.ExcelFile(excel_file_path)

    # Iterate through each sheet and save it as a CSV file
    for sheet_name in xls.sheet_names:
        # Read the sheet
        df = pd.read_excel(xls, sheet_name)

        # Save the sheet as a CSV file
        csv_file_name = f"{sheet_name}.csv"
        df.to_csv(csv_file_name, index=False)

    return f"All sheets from {excel_file_path} have been saved as CSV files."

# Example usage:
save_excel_sheets_as_csv('./data/实体表删除第一sheet.xlsx')
