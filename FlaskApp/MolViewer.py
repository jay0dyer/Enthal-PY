from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem import rdDepictor
import matplotlib as mpl
import matplotlib.colors as colors

def DisplayMolA(mol):
    mol = mol.EnthalpyMapMol

    rdDepictor.SetPreferCoordGen(True)
    rdDepictor.Compute2DCoords(mol)
    drawer = rdMolDraw2D.MolDraw2DCairo(2000,2000)
    options = drawer.drawOptions()

    #visaul settings
    options.clearBackground = True
    options.bondLineWidth = 5
    options.highlightBondWidthMultiplier = 3
    options.continuousHighlight = True

    enthalpies = []
    for bond in mol.GetBonds():
        enthalpies.append(bond.GetDoubleProp("Enthalpy"))

    #vmin=(min(enthalpies)-1), vmax=max(enthalpies)
    norm = colors.TwoSlopeNorm(vcenter=(sum(enthalpies)/len(enthalpies)), vmin=0, vmax=0.6)
    colormap = mpl.colormaps['managua'] # R means reveresed

    highlight_bonds = []
    highlight_colors = {}

    for bond in mol.GetBonds():
        b_idx = bond.GetIdx()

        if bond.HasProp("Enthalpy"):
            Enthalpy = bond.GetDoubleProp("Enthalpy")
            #print(Enthalpy)

            # Map the float value to an RGB color tuple
            rgba = colormap(norm(Enthalpy))
            rgb_tuple = (rgba[0], rgba[1], rgba[2], 0.8)

            highlight_bonds.append(b_idx)
            highlight_colors[b_idx] = rgb_tuple

    rdMolDraw2D.PrepareAndDrawMolecule(
        drawer,
        mol,
        highlightBonds=highlight_bonds,
        highlightBondColors=highlight_colors
    )
    drawer.FinishDrawing()

    with open("static/styles/output.png", "wb") as f:
        f.write(drawer.GetDrawingText())

