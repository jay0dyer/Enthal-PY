import gzip
import shutil

with open("QM9StarDataProcessing/DATA/EnthalpyTables.db", "rb") as file_in:
    with gzip.open("FlaskApp/Database/EnthalpyTables.gz", "wb") as file_out:
        shutil.copyfileobj(file_in, file_out)

