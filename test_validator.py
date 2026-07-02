from utils.excel_validator import ExcelValidator

validator = ExcelValidator()

status, result = validator.validate("data/Calibration.xlsx")

if status:

    print("Validation Successful")

    print(result.head())

else:

    print(result)