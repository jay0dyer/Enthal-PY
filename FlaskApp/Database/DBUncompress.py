import gzip
import shutil

def uncompressDB():
    with gzip.open("EnthalpyTables.gz", "rb") as file_in:
        with open("Temp/EnthalpyTables.db", "wb") as file_out:
            shutil.copyfileobj(file_in, file_out)

if __name__ == "__main__":
    uncompressDB()