import gzip
import shutil

def uncompressDB():
    with gzip.open("Database/EnthalpyTables.gz", "rb") as file_in:
        with open("Database/Temp/EnthalpyTables.db", "wb") as file_out:
            shutil.copyfileobj(file_in, file_out)