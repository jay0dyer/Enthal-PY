import sqlite3
import pandas as pd

# created after bulk of data processing

missing_radical = pd.DataFrame([ # data provided by gemmini
    {"SMILES": "[H]", "HF": -0.5000, "Radical Type": 1},  # H neutral (Radical)
    {"SMILES": "[H+]", "HF": 0.0000, "Radical Type": 0},  # H+ (Fully stripped)
    {"SMILES": "[H-]", "HF": -0.4879, "Radical Type": 2},  # H- (Hydride anion, lone pair)

    # --- Carbon Ionization States (Z = 6) ---
    {"SMILES": "[C]", "HF": -37.6886, "Radical Type": 0},           # C Neutral
    {"SMILES": "[C+]", "HF": -37.2882, "Radical Type": 1},          # C+1
    {"SMILES": "[C+2]", "HF": -36.3861, "Radical Type": 2},         # C+2
    {"SMILES": "[C+3]", "HF": -34.7214, "Radical Type": 3},         # C+3
    {"SMILES": "[C+4]", "HF": -32.3612, "Radical Type": 4},         # C+4
    {"SMILES": "[C+5]", "HF": -15.6806, "Radical Type": 5},         # C+5
    {"SMILES": "[C+6]", "HF": 0.0000, "Radical Type": 6},           # C+6 (Stripped nucleus)

    # --- Nitrogen Ionization States (Z = 7) ---
    {"SMILES": "[N]", "HF": -54.4009, "Radical Type": 0},           # N Neutral
    {"SMILES": "[N+]", "HF": -53.8619, "Radical Type": 1},          # N+1
    {"SMILES": "[N+2]", "HF": -52.7766, "Radical Type": 2},         # N+2
    {"SMILES": "[N+3]", "HF": -51.3789, "Radical Type": 3},         # N+3
    {"SMILES": "[N+4]", "HF": -49.2778, "Radical Type": 4},         # N+4
    {"SMILES": "[N+5]", "HF": -46.3686, "Radical Type": 5},         # N+5
    {"SMILES": "[N+6]", "HF": -22.1264, "Radical Type": 6},         # N+6
    {"SMILES": "[N+7]", "HF": 0.0000, "Radical Type": 7},           # N+7 (Stripped nucleus)

    # --- Oxygen Ionization States (Z = 8) ---
    {"SMILES": "[O]", "HF": -74.8094, "Radical Type": 0},           # O Neutral
    {"SMILES": "[O+]", "HF": -74.2889, "Radical Type": 1},          # O+1
    {"SMILES": "[O+2]", "HF": -73.0039, "Radical Type": 2},         # O+2
    {"SMILES": "[O+3]", "HF": -71.3283, "Radical Type": 3},         # O+3
    {"SMILES": "[O+4]", "HF": -69.3175, "Radical Type": 4},         # O+4
    {"SMILES": "[O+5]", "HF": -66.5898, "Radical Type": 5},         # O+5
    {"SMILES": "[O+6]", "HF": -63.0298, "Radical Type": 6},         # O+6
    {"SMILES": "[O+7]", "HF": -29.5723, "Radical Type": 7},         # O+7
    {"SMILES": "[O+8]", "HF": 0.0000, "Radical Type": 8},           # O+8 (Stripped nucleus)

    # --- First Neutral Radical Atoms: Group 1 (Alkali Metals) ---
    {"SMILES": "[Li]", "HF": -7.4327, "Radical Type": 0},           # Li Neutral
    {"SMILES": "[Na]", "HF": -161.8589, "Radical Type": 0},         # Na Neutral
    {"SMILES": "[K]", "HF": -599.1648, "Radical Type": 0},          # K Neutral
    {"SMILES": "[Rb]", "HF": -2938.2809, "Radical Type": 0},        # Rb Neutral
    {"SMILES": "[Cs]", "HF": -7532.1812, "Radical Type": 0},        # Cs Neutral

    # --- First Neutral Radical Atoms: Group 17 (Halogens) ---
    {"SMILES": "[F]", "HF": -99.4093, "Radical Type": 0},           # F Neutral
    {"SMILES": "[Cl]", "HF": -459.4821, "Radical Type": 0},         # Cl Neutral
    {"SMILES": "[Br]", "HF": -2572.4416, "Radical Type": 0},        # Br Neutral
    {"SMILES": "[I]", "HF": -6917.9814, "Radical Type": 0}          # I Neutral
])

table_creation_query = """
    CREATE TABLE IF NOT EXISTS Radical_{i} (
        SMILES VARCHAR(255) NOT NULL,
        HF INT
    );
"""
for i in range(8):
    cursor.execute(table_creation_query.format(i=i))

for i in range(8):
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_smiles_{i} ON Radical_{i}(SMILES)")

conn.commit()

conn = sqlite3.connect("DATA/EnthalpyTables.db")
cursor = conn.cursor()

for row in missing_radical:
    cursor.execute("INSERT INTO Radical_{i} VALUES ('{SMILES}', {HF})".format(
        i=int(row["Radical Type"]), SMILES=row["SMILES"], HF=round(row["HF"])))

conn.commit()