import pandas as pd

qm9csv = pd.read_csv("DATA/qm9.csv")

qm9TOAPPEND = pd.DataFrame(columns=['SMILES', 'HF', 'Radical Type'])
qm9TOAPPEND["SMILES"] = qm9csv['smiles']
qm9TOAPPEND["HF"] = qm9csv['h298']
qm9TOAPPEND["Radical Type"] = 0

qm9star = pd.read_csv("DATA/SMILESEnthalpyLookUp.csv")

missing_gases = pd.DataFrame([ # data provided by gemmini
    {"SMILES": "O=C=O", "HF": -188.6, "Radical Type": 0}, # CO2
    {"SMILES": "O=O", "HF": -150.3, "Radical Type": 0},     # O2
    {"SMILES": "N#N", "HF": -109.5, "Radical Type": 0},     # N2
    {"SMILES": "[C-]#[O+]", "HF": -113.3, "Radical Type": 0} # CO
])

# Append them to the bottom of your dataset

combined = pd.concat([qm9star, qm9TOAPPEND], ignore_index=True)
combined = pd.concat([combined, missing_gases], ignore_index=True)
combined = combined.drop_duplicates(subset=['SMILES'], keep='first')

combined.to_csv("DATA/SMILESEnthalpyLookUpAPPEND.csv", index=False)