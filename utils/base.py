import os
import pandas as pd

from pyaedt import Edb

from pyaedt.generic.general_methods import generate_unique_name


class ReadEdbBaseFunc:

    def __init__(self, edb_fpath, project_name="unnamed", edb_version="2022.1"):
        self.edb_version = edb_version

        self.unique_name = generate_unique_name("_pcb")

        self.edbapp = Edb(edbpath=edb_fpath, edbversion=edb_version)

        self.project_name = project_name + self.unique_name

    def save_edb_as(self, fdir):
        fdir = fdir.replace("//", "\\")
        fpath = os.path.join(fdir, self.project_name + ".aedb")
        self.edbapp.save_edb_as(fpath)
        print("AEDT project is save as {}".format(fpath))
        self.edbapp.close_edb()
        return fpath


class ReadIbis:
    POWER = ["VDD", "VDDQ", "VREFCA", "VREFDQ"]
    GND = ["VSS", "VSSQ"]
    OTHER = ["NF", "RST#", "NC", "ZQ", "NF_TDQS#", "DM_TDQS"]

    def __init__(self, fpath):
        self.fpath = fpath

    def read_pin(self):
        df = pd.read_csv(self.fpath, delimiter=r"\s+", usecols=["[Pin]", "signal_name"])
        df = df[~df["signal_name"].isin(self.POWER + self.GND + self.OTHER)]
        tmp = []
        for _, row in df.iterrows():
            signal_name = row["signal_name"]
            if signal_name.startswith("DQS"):
                tmp.append("DQS")
            elif signal_name.startswith("DQ"):
                tmp.append("DQ")
            elif signal_name.startswith("CK"):
                tmp.append("CK")
            else:
                tmp.append("CA")

        df["Group"] = tmp

        df = df.sort_values(by="Group")
        df.to_csv(os.path.join(os.path.dirname(self.fpath), "pins.txt"), index=False, header=False)


if __name__ == '__main__':
    ReadIbis(fpath="example_ddr_port_setup/ibs.txt").read_pin()
