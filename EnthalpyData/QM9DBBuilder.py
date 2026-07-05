import pandas as pd
import sqlite3

filename = "RawData/qm9.csv"
FullData = pd.read_csv(filename)

RequiredData = FullData[["smiles","h298"]]

print(RequiredData)

conn = sqlite3.connect("SMILESLookUpData/EnthalpyData.db")

RequiredData.to_sql(name="QM9", con=conn, if_exists="replace", index=False)
conn.close()