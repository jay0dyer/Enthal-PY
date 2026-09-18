import sqlite3
import pandas as pd

# Read the CSV file
CSVForm = pd.read_csv("DATA/SMILESEnthalpyLookUpAPPEND.csv")
sizecsv = CSVForm.shape[0]

CSVForm = CSVForm.sort_values("Radical Type")
conn = sqlite3.connect("DATA/EnthalpyTables.db")
cursor = conn.cursor()

table_creation_query = """
    CREATE TABLE IF NOT EXISTS Radical_{i} (
        SMILES VARCHAR(255) NOT NULL,
        HF INT
    );
"""
for i in range(3):
    cursor.execute(table_creation_query.format(i=i))

conn.commit()
CSVForm["Radical Type"].fillna(0).astype(int)

print(sizecsv)
p = 0
for i, row in CSVForm.iterrows():

    cursor.execute("INSERT INTO Radical_{i} VALUES ('{SMILES}', {HF})".format(
        i=int(row["Radical Type"]),SMILES=row["SMILES"],HF=round(row["HF"])))
    p += 1
    print((p/sizecsv)*100,"%")

for i in range(3):
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_smiles_{i} ON Radical_{i}(SMILES)")

conn.commit()