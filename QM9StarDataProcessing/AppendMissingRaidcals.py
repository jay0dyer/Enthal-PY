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

        {"SMILES": "[CH2][CH2]", "HF": -78.5153, "Radical Type": 2},  # 2 bonds broken
        {"SMILES": "[CH][CH]", "HF": -77.2006, "Radical Type": 4},  # 4 bonds broken
        {"SMILES": "[C][C]", "HF": -75.8858, "Radical Type": 6},  # 6 bonds broken (The one causing your error!)
        {"SMILES": "[CH2]C", "HF": -79.1726, "Radical Type": 1},  # 1 bond broken
        {"SMILES": "[CH]C", "HF": -78.5153, "Radical Type": 2},  # 2 bonds broken
        {"SMILES": "[C]C", "HF": -77.8579, "Radical Type": 3},  # 3 bonds broken (Your current error)
        {"SMILES": "[CH2][CH]", "HF": -77.8579, "Radical Type": 3},  # 3 bonds broken (Alternative distribution)
        {"SMILES": "[C][CH2]", "HF": -77.2006, "Radical Type": 4},  # 4 bonds broken
        {"SMILES": "[C][CH]", "HF": -76.5432, "Radical Type": 5},  # 5 bonds broken

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

        {"SMILES": "LiH", "HF": -8.0199, "Radical Type": 0},
        {"SMILES": "Li", "HF": -7.4327, "Radical Type": 1},
        {"SMILES": "[Li]", "HF": -7.4327, "Radical Type": 1},

        {"SMILES": "NaH", "HF": -162.4286, "Radical Type": 0},
        {"SMILES": "Na", "HF": -161.8589, "Radical Type": 1},
        {"SMILES": "[Na]", "HF": -161.8589, "Radical Type": 1},

        {"SMILES": "F", "HF": -99.3642, "Radical Type": 0},
        {"SMILES": "[F]", "HF": -99.3642, "Radical Type": 1},

        {"SMILES": "Cl", "HF": -459.4800, "Radical Type": 0},
        {"SMILES": "[Cl]", "HF": -459.4800, "Radical Type": 1},

        {"SMILES": "Br", "HF": -2572.4400, "Radical Type": 0},
        {"SMILES": "[Br]", "HF": -2572.4400, "Radical Type": 1},

        # --- Fluorine Environments ---
        {"SMILES": "CF", "HF": -139.3705, "Radical Type": 0},
        {"SMILES": "FC", "HF": -139.3705, "Radical Type": 0},

        {"SMILES": "[CH2]F", "HF": -138.6972, "Radical Type": 1},
        {"SMILES": "F[CH2]", "HF": -138.6972, "Radical Type": 1},

        {"SMILES": "[CH]F", "HF": -137.7805, "Radical Type": 2},
        {"SMILES": "F[CH]", "HF": -137.7805, "Radical Type": 2},

        {"SMILES": "[C]F", "HF": -137.1550, "Radical Type": 3},
        {"SMILES": "F[C]", "HF": -137.1550, "Radical Type": 3},

        # --- Chlorine Environments ---
        {"SMILES": "CCl", "HF": -499.4369, "Radical Type": 0},
        {"SMILES": "ClC", "HF": -499.4369, "Radical Type": 0},

        {"SMILES": "[CH2]Cl", "HF": -498.7636, "Radical Type": 1},
        {"SMILES": "Cl[CH2]", "HF": -498.7636, "Radical Type": 1},

        {"SMILES": "[CH]Cl", "HF": -497.8469, "Radical Type": 2},
        {"SMILES": "Cl[CH]", "HF": -497.8469, "Radical Type": 2},

        {"SMILES": "[C]Cl", "HF": -497.2214, "Radical Type": 3},
        {"SMILES": "Cl[C]", "HF": -497.2214, "Radical Type": 3},

        # --- Bromine Environments ---
        {"SMILES": "CBr", "HF": -2612.3746, "Radical Type": 0},
        {"SMILES": "BrC", "HF": -2612.3746, "Radical Type": 0},

        {"SMILES": "[CH2]Br", "HF": -2611.7013, "Radical Type": 1},
        {"SMILES": "Br[CH2]", "HF": -2611.7013, "Radical Type": 1},

        {"SMILES": "[CH]Br", "HF": -2610.7846, "Radical Type": 2},
        {"SMILES": "Br[CH]", "HF": -2610.7846, "Radical Type": 2},

        {"SMILES": "[C]Br", "HF": -2610.1591, "Radical Type": 3},
        {"SMILES": "Br[C]", "HF": -2610.1591, "Radical Type": 3},

        # --- Lithium Environments ---
        {"SMILES": "CLi", "HF": -47.3465, "Radical Type": 0},
        {"SMILES": "LiC", "HF": -47.3465, "Radical Type": 0},
        {"SMILES": "C[Li]", "HF": -47.3465, "Radical Type": 0},
        {"SMILES": "[Li]C", "HF": -47.3465, "Radical Type": 0},

        {"SMILES": "[CH2]Li", "HF": -46.6732, "Radical Type": 1},
        {"SMILES": "Li[CH2]", "HF": -46.6732, "Radical Type": 1},
        {"SMILES": "[CH2][Li]", "HF": -46.6732, "Radical Type": 1},
        {"SMILES": "[Li][CH2]", "HF": -46.6732, "Radical Type": 1},

        {"SMILES": "[CH]Li", "HF": -45.7565, "Radical Type": 2},
        {"SMILES": "Li[CH]", "HF": -45.7565, "Radical Type": 2},
        {"SMILES": "[CH][Li]", "HF": -45.7565, "Radical Type": 2},
        {"SMILES": "[Li][CH]", "HF": -45.7565, "Radical Type": 2},

        {"SMILES": "[C]Li", "HF": -45.1310, "Radical Type": 3},
        {"SMILES": "Li[C]", "HF": -45.1310, "Radical Type": 3},
        {"SMILES": "[C][Li]", "HF": -45.1310, "Radical Type": 3},
        {"SMILES": "[Li][C]", "HF": -45.1310, "Radical Type": 3},

        # --- Sodium Environments ---
        {"SMILES": "CNa", "HF": -201.7536, "Radical Type": 0},
        {"SMILES": "NaC", "HF": -201.7536, "Radical Type": 0},
        {"SMILES": "C[Na]", "HF": -201.7105, "Radical Type": 0},
        {"SMILES": "[Na]C", "HF": -201.7105, "Radical Type": 0},

        {"SMILES": "[CH2]Na", "HF": -201.0803, "Radical Type": 1},
        {"SMILES": "Na[CH2]", "HF": -201.0803, "Radical Type": 1},
        {"SMILES": "[CH2][Na]", "HF": -201.0803, "Radical Type": 1},
        {"SMILES": "[Na][CH2]", "HF": -201.0803, "Radical Type": 1},

        {"SMILES": "[CH]Na", "HF": -200.1636, "Radical Type": 2},
        {"SMILES": "Na[CH]", "HF": -200.1636, "Radical Type": 2},
        {"SMILES": "[CH][Na]", "HF": -200.1636, "Radical Type": 2},
        {"SMILES": "[Na][CH]", "HF": -200.1636, "Radical Type": 2},

        {"SMILES": "[C]Na", "HF": -199.5381, "Radical Type": 3},
        {"SMILES": "Na[C]", "HF": -199.5381, "Radical Type": 3},
        {"SMILES": "[C][Na]", "HF": -199.5381, "Radical Type": 3},
        {"SMILES": "[Na][C]", "HF": -199.5381, "Radical Type": 3}
    ]

    conn = sqlite3.connect("DATA/EnthalpyTables.db")
    cursor = conn.cursor()
    for row in missing_radicals:
        cursor.execute("INSERT INTO Radical_{i} VALUES ('{SMILES}', {HF})".format(
            i=int(row["Radical Type"]), SMILES=row["SMILES"], HF=round(row["HF"],3)))

    conn.commit()

if __name__ == "main":
    AppendMissingRadicals()