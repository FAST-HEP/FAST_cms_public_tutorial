from uproot_methods import TLorentzVectorArray
import numpy as np


class DiMuonMass():
    def __init__(self, name, out_dir, mask=None, collection="Muon", out_var="DiIsoMuon"):
        self.name = name
        self.out_dir = out_dir
        self.mask = mask
        self.collection = collection

        self.branches = [self.collection + "_" + var for var in ["Px", "Py", "Pz", "E"]]
        self.out_var = out_var + "_Mass"

    def event(self, chunk):
        # Get the data as a pandas dataframe
        px, py, pz, energy = chunk.tree.arrays(self.branches, outputtype=tuple)

        # Rename the branches so they're easier to work with here
        if self.mask:
            mask = chunk.tree.array(self.mask)
            px = px[mask]
            py = py[mask]
            pz = pz[mask]
            energy = energy[mask]

        # Find the second object in the event (which are sorted by Pt)
        has_two_obj = px.counts > 1

        # Calculate the invariant mass
        p4_0 = TLorentzVectorArray(px[has_two_obj, 0], py[has_two_obj, 0], pz[has_two_obj, 0], energy[has_two_obj, 0])
        p4_1 = TLorentzVectorArray(px[has_two_obj, 1], py[has_two_obj, 1], pz[has_two_obj, 1], energy[has_two_obj, 1])
        di_object = p4_0 + p4_1

        # insert nans for events that have fewer than 2 objects
        masses = np.full(len(chunk.tree), np.nan)
        masses[has_two_obj] = di_object.mass

        # Add this variable to the tree
        chunk.tree.new_variable(self.out_var, masses)
        return True
