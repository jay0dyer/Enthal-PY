import pandas as pd
import sqlite3

filename = "RawData/qm9.csv"
FullData = pd.read_csv(filename)

RequiredData = FullData[["smiles","h298"]]

print(RequiredData)

conn = sqlite3.connect("SMILESLookUpData/EnthalpyData.db")

# 3. Save the DataFrame to a table named 'users'
RequiredData.to_sql(name="QM9", con=conn, if_exists="replace", index=False)

# 4. Close the connection
conn.close()