import sqlite3

# created after bulk of data processing

def AppendMissingRadicals():
    missing_radicals = [
        {"SMILES": "[H][H]", "HF": -1.1268, "Radical Type": 0},  # H2 (H-H single)
        {"SMILES": "C", "HF": -40.1951, "Radical Type": 0},  # CH4 (C-H single)
        {"SMILES": "N", "HF": -56.1655, "Radical Type": 0},  # NH3 (N-H single)
        {"SMILES": "O", "HF": -76.0107, "Radical Type": 0},  # H2O (O-H single)
        {"SMILES": "CC", "HF": -79.2288, "Radical Type": 0},  # C2H6 (C-C single)
        {"SMILES": "C=C", "HF": -78.0317, "Radical Type": 0},  # C2H4 (C=C double)
        {"SMILES": "C#C", "HF": -76.8178, "Radical Type": 0},  # C2H2 (C#C triple)
        {"SMILES": "CN", "HF": -95.2090, "Radical Type": 0},  # CH3NH2 (C-N single)
        {"SMILES": "C=N", "HF": -94.0242, "Radical Type": 0},  # CH2NH (C=N double)
        {"SMILES": "C#N", "HF": -92.8252, "Radical Type": 0},  # HCN (C#N triple)
        {"SMILES": "CO", "HF": -115.0354, "Radical Type": 0},  # CH3OH (C-O single)
        {"SMILES": "C=O", "HF": -113.8494, "Radical Type": 0},  # CH2O (C=O double)
        {"SMILES": "NN", "HF": -111.1683, "Radical Type": 0},  # N2H4 (N-N single)
        {"SMILES": "N=N", "HF": -109.9831, "Radical Type": 0},  # N2H2 (N=N double)
        {"SMILES": "NO", "HF": -130.9821, "Radical Type": 0},  # NH2OH (N-O single)
        {"SMILES": "OO", "HF": -150.7858, "Radical Type": 0},

        # --- Reference Closed-Shell Molecules ---
        {"SMILES": "O=C=O", "HF": -187.6342, "Radical Type": 0},  # CO2
        {"SMILES": "O=O", "HF": -149.6133, "Radical Type": 0},  # O2 (Triplet HF ground state)
        {"SMILES": "N#N", "HF": -108.9439, "Radical Type": 0},  # N2
        {"SMILES": "[C-]#[O+]", "HF": -112.7379, "Radical Type": 0},  # CO

        # --- Hydrogen Species ---
        {"SMILES": "[H]", "HF": -0.4982, "Radical Type": 1},  # H neutral (Radical)
        {"SMILES": "[H+]", "HF": 0.0000, "Radical Type": 0},  # H+ (Fully stripped proton)
        {"SMILES": "[H-]", "HF": -0.4214, "Radical Type": 2},  # H- (Hydride anion)

        # --- Carbon Hydrogen Depletion Series (Base: CH4 = -40.1951) ---
        {"SMILES": "[CH3]", "HF": -39.5593, "Radical Type": 1},  # Methyl radical
        {"SMILES": "[CH2]", "HF": -38.9142, "Radical Type": 2},  # Methylene
        {"SMILES": "[CH]", "HF": -38.2325, "Radical Type": 3},  # Methyne
        {"SMILES": "[C]", "HF": -37.6401, "Radical Type": 4},  # Atomic Carbon

        # --- Nitrogen Hydrogen Depletion Series (Base: NH3 = -56.1655) ---
        {"SMILES": "N", "HF": -56.1655, "Radical Type": 0},  # Ammonia (NH3)
        {"SMILES": "[NH2]", "HF": -55.5188, "Radical Type": 1},  # Amino radical
        {"SMILES": "[NH]", "HF": -54.8872, "Radical Type": 2},  # Imidogen
        {"SMILES": "[N]", "HF": -54.3855, "Radical Type": 3},  # Atomic Nitrogen

        # --- Oxygen Hydrogen Depletion Series (Base: H2O = -76.0107) ---
        {"SMILES": "O", "HF": -76.0107, "Radical Type": 0},  # Water (H2O)
        {"SMILES": "[OH]", "HF": -75.3651, "Radical Type": 1},  # Hydroxyl radical
        {"SMILES": "[O]", "HF": -74.7839, "Radical Type": 2},  # Atomic Oxygen

        # --- Group 1 Alkali Metals (Properly splitting M from H) ---
        {"SMILES": "[LiH]", "HF": -7.9864, "Radical Type": 0},
        {"SMILES": "[Li]", "HF": -7.4327, "Radical Type": 1},
        {"SMILES": "[NaH]", "HF": -162.3921, "Radical Type": 0},
        {"SMILES": "[Na]", "HF": -161.8589, "Radical Type": 1},

        # --- Group 17 Halogens ---
        {"SMILES": "[FH]", "HF": -100.0028, "Radical Type": 0},  # HF Molecule
        {"SMILES": "[F]", "HF": -99.3642, "Radical Type": 1}  # Fluorine Atom
    ]

    conn = sqlite3.connect("DATA/EnthalpyTables.db")
    cursor = conn.cursor()
    for row in missing_radicals:
        cursor.execute("INSERT INTO Radical_{i} VALUES ('{SMILES}', {HF})".format(
            i=int(row["Radical Type"]), SMILES=row["SMILES"], HF=round(row["HF"],3)))

    conn.commit()

if __name__ == "main":
    AppendMissingRadicals()