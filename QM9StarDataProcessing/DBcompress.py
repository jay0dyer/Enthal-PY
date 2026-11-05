import gzip
import shutil

def compressDB():
    with  open("DATA/EnthalpyTables.db", "rb")  as file_in:
        with gzip.open("../FlaskApp/Database/EnthalpyTables.gz", "wb") as file_out:
            shutil.copyfileobj(file_in, file_out)

if __name__ == "__main__":
    compressDB()