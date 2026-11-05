import sqlite3
import pandas as pd

# created after bulk of data processing

missing_radical = [ # data provided by gemmini
    {"SMILES": "O=C=O", "HF": -188.6, "Radical Type": 0}, # CO2
    {"SMILES": "O=O", "HF": -150.3, "Radical Type": 0},     # O2
    {"SMILES": "N#N", "HF": -109.5, "Radical Type": 0},     # N2
    {"SMILES": "[C-]#[O+]", "HF": -113.3, "Radical Type": 0}, # CO

    {"SMILES": "[H]", "HF": -0.5000, "Radical Type": 1},  # H neutral (Radical)
    {"SMILES": "[H+]", "HF": 0.0000, "Radical Type": 0},  # H+ (Fully stripped)
    {"SMILES": "[H-]", "HF": -0.4879, "Radical Type": 2},  # H- (Hydride anion, lone pair)

    # --- Carbon Hydrogen Depletion Series (Base: CH4, Max H = 4) ---
    # --- Carbon Hydrogen Depletion Series (Base: CH4, Max H = 4) ---
    {"SMILES": "[CH4]", "HF": -37.6886, "Radical Type": 0},  # 0 missing H (Methane)
    {"SMILES": "[CH3]", "HF": -37.2882, "Radical Type": 1},  # 1 missing H (Methyl radical)
    {"SMILES": "[CH2]", "HF": -36.3861, "Radical Type": 2},  # 2 missing H (Methylene)
    {"SMILES": "[CH]", "HF": -34.7214, "Radical Type": 3},  # 3 missing H (Methyne)
    {"SMILES": "[C]", "HF": -32.3612, "Radical Type": 4},  # 4 missing H (Atomic Carbon)

    # --- Nitrogen Hydrogen Depletion Series (Base: NH3, Max H = 3) ---
    {"SMILES": "[NH3]", "HF": -54.4009, "Radical Type": 0},  # 0 missing H (Ammonia)
    {"SMILES": "[NH2]", "HF": -53.8619, "Radical Type": 1},  # 1 missing H (Amino radical)
    {"SMILES": "[NH]", "HF": -52.7766, "Radical Type": 2},  # 2 missing H (Imidogen)
    {"SMILES": "[N]", "HF": -51.3789, "Radical Type": 3},  # 3 missing H (Atomic Nitrogen)

    # --- Oxygen Hydrogen Depletion Series (Base: H2O, Max H = 2) ---
    {"SMILES": "[OH2]", "HF": -74.8094, "Radical Type": 0},  # 0 missing H (Water)
    {"SMILES": "[OH]", "HF": -74.2889, "Radical Type": 1},  # 1 missing H (Hydroxyl radical)
    {"SMILES": "[O]", "HF": -73.0039, "Radical Type": 2},  # 2 missing H (Atomic Oxygen)

    # --- Group 1 Alkali Metals (Base: MH, Max H = 1) ---
    {"SMILES": "[LiH]", "HF": -7.4327, "Radical Type": 0},  # 0 missing H
    {"SMILES": "[Li]", "HF": -7.4327, "Radical Type": 1},  # 1 missing H
    {"SMILES": "[NaH]", "HF": -161.8589, "Radical Type": 0},  # 0 missing H
    {"SMILES": "[Na]", "HF": -161.8589, "Radical Type": 1},  # 1 missing H
    {"SMILES": "[KH]", "HF": -599.1648, "Radical Type": 0},  # 0 missing H
    {"SMILES": "[K]", "HF": -599.1648, "Radical Type": 1},  # 1 missing H
    {"SMILES": "[RbH]", "HF": -2938.2809, "Radical Type": 0},  # 0 missing H
    {"SMILES": "[Rb]", "HF": -2938.2809, "Radical Type": 1},  # 1 missing H
    {"SMILES": "[CsH]", "HF": -7532.1812, "Radical Type": 0},  # 0 missing H
    {"SMILES": "[Cs]", "HF": -7532.1812, "Radical Type": 1},  # 1 missing H

    # --- Group 17 Halogens (Base: HX, Max H = 1) ---
    {"SMILES": "[FH]", "HF": -99.4093, "Radical Type": 0},  # 0 missing H
    {"SMILES": "[F]", "HF": -99.4093, "Radical Type": 1},  # 1 missing H
    {"SMILES": "[ClH]", "HF": -459.4821, "Radical Type": 0}
]

table_creation_query = """
    CREATE TABLE IF NOT EXISTS Radical_{i} (
        SMILES VARCHAR(255) NOT NULL,
        HF INT
    );
"""

conn = sqlite3.connect("DATA/EnthalpyTables.db")
cursor = conn.cursor()
conn.commit()

conn = sqlite3.connect("DATA/EnthalpyTables.db")
cursor = conn.cursor()

def AppendMissingRadicals():
    for row in missing_radical:
        cursor.execute("INSERT INTO Radical_{i} VALUES ('{SMILES}', {HF})".format(
            i=int(row["Radical Type"]), SMILES=row["SMILES"], HF=round(row["HF"])))

conn.commit()