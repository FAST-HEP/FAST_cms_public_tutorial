from uproot_methods import TLorentzVector, TLorentzVectorArray
import numpy as np
import pandas as pd
from fast_carpenter.define import parents2startsstops
import awkward

class MuonPt():
    def __init__(self, name, out_dir, collection):
        self.name = name
        self.out_dir = out_dir
        self.collection = collection

    def event(self, chunk):
        data = chunk.tree.pandas.df(["Muon_Px", "Muon_Py"])
        pt_numexpr = data.eval("sqrt(Muon_Px ** 2 + Muon_Py ** 2)")
        pt_numexpr_jagged = awkward.JaggedArray.fromparents(pt_numexpr.index.get_level_values(0).values, pt_numexpr.values)

        chunk.tree.new_variable("test_Pt", pt_numexpr_jagged)


class IsoMuons():
    def __init__(self, name, out_dir, iso_var="Muon_isolation", pt_var="Muon_Pt", threshold=0.2, output="IsoMuon"):
        self.name = name
        self.out_dir = out_dir
        self.iso_var = iso_var
        self.pt_var = pt_var
        self.threshold = threshold
        self.output = output
        self.branches = {iso_var: "iso", pt_var: "pt"}

    def event(self, chunk):
        data = chunk.tree.pandas.df(self.branches.keys()).rename(columns=self.branches)
        iso = data.iso
        pt = data.pt
        is_isolation = (iso / pt) < self.threshold
        is_isolation = awkward.JaggedArray.fromparents(is_isolation.index.get_level_values(0).values, is_isolation.values)
        n_iso_muon = is_isolation.count_nonzero()
        chunk.tree.new_variable(self.output + "_Idx", is_isolation)
        chunk.tree.new_variable("N" + self.output, n_iso_muon)


class DiMuonMass():
    def __init__(self, name, out_dir, mask=None, collection="Muon", out_var="DiIsoMuon"):
        self.name = name
        self.out_dir = out_dir
        self.mask = mask
        self.collection = collection

        self.branches = {self.collection + "_" + var: var for var in ["Px", "Py", "Pz", "E"]}
        self.out_var = out_var + "_Mass"

    def event(self, chunk):
        # Get the data as a pandas dataframe
        data = chunk.tree.pandas.df(self.branches.keys())

        # Need this later on...
        first_event = data.index.get_level_values(0).values[0]

        # Rename the branches so they're easier to work with here
        data.rename(columns=self.branches, inplace=True)
        if self.mask:
            mask = chunk.tree.pandas.df(self.mask)
            mask = mask[mask[self.mask]]
            data = mask.merge(data, how="left", left_index=True, right_index=True)

        # Find the second object in the event (which are sorted by Pt)
        object2 = data.groupby(level=0).nth(1)
        have_two_objects = object2.index
        # If there was a second object, get the first object
        object1 = data.loc[have_two_objects].groupby(level=0).nth(0)

        # Calculate the invariant mass
        p4_1 = TLorentzVectorArray(object1.Px, object1.Py, object1.Pz, object1.E)
        p4_2 = TLorentzVectorArray(object2.Px, object2.Py, object2.Pz, object2.E)
        di_object = p4_1 + p4_2

        # insert nans for events that have fewer than 2 objects
        masses = np.ones(len(chunk.tree)) * np.nan
        have_two_objects -= first_event
        masses[have_two_objects] = di_object.mass

        # Add this variable to the tree
        chunk.tree.new_variable(self.out_var, masses)
        return True
