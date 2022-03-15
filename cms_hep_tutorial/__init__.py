import awkward as ak
import vector
import numpy as np

from fast_carpenter.tree_adapter import ArrayMethods

class DiObjectMass():
    def __init__(self, name, out_dir, collection="Muon", mask=None, out_var=None):
        self.name = name
        self.out_dir = out_dir
        self.mask = mask
        self.collection = collection

        self.branches = [self.collection + "_" + var for var in ["Px", "Py", "Pz", "E"]]
        if out_var:
            self.out_var = out_var
        else:
            self.out_var = "Di{}_Mass".format(collection)

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
        has_two_obj = ArrayMethods.counts(px) > 1

        # Calculate the invariant mass
        p4_0 = vector.array({
            "x": px[has_two_obj][:, 0],
            "y": py[has_two_obj][:, 0],
            "z": pz[has_two_obj][:, 0],
            "t": energy[has_two_obj][:, 0],
        })
        p4_1 = vector.array({
            "x": px[has_two_obj][:, 1],
            "y": py[has_two_obj][:, 1],
            "z": pz[has_two_obj][:, 1],
            "t": energy[has_two_obj][:, 1],
        })
        di_object = p4_0 + p4_1

        # insert nans for events that have fewer than 2 objects
        masses = np.full(len(chunk.tree), np.nan)
        masses[has_two_obj] = di_object.tau

        # Add this variable to the tree
        chunk.tree.new_variable(self.out_var, masses)
        return True
