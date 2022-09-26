import csv
import os
import json
import pandas as pd
from pyaedt import Edb


def correct_port_name(name):
    target = ["$", "<", ">"]
    for t in target:
        name = name.replace(t, "_")
    return name


class DDRPortSetup:
    EDB_VERSION = "2022.2"
    GND_NET_NAME = "GND"
    DRAM_TYPE_LIST = {"ddr5_x16": "ddr5_x16.json",
                      "ddr3_x8": "ddr3_x8.json"}

    def __init__(self,
                 edb_fpath,
                 controller_refdes,
                 dram_refdes,
                 dram_type,
                 ):

        if not isinstance(dram_refdes, list):
            dram_refdes = [dram_refdes]

        with open(os.path.join("_ddrx_pin_mapping", self.DRAM_TYPE_LIST[dram_type]), encoding="utf-8") as f:
            data = json.load(f)

        self.edbapp = Edb(edbpath=edb_fpath, edbversion=self.EDB_VERSION)

        ###############################################################################################
        # Find ports on DRAMs
        dq_group_name = ["DQ", "DQ_0", "DQ_1"]
        dqs_group_name = ["DQS", "DQS_0", "DQS_1"]

        controller_net_list = []  # jedec_sname net_name
        self.port_list = []  # refdes pin_name net_name port_name
        port_index = 0
        first_dram = True
        dq_signal_index = 0
        dqs_t_signal_index = 0
        dqs_c_signal_index = 0
        for refdes in dram_refdes:
            comp = self.edbapp.core_components.components[refdes]

            # clock signals
            signal_type = "CK"
            signal_index = 0
            for jedec_sname, pin_name in data[signal_type].items():
                net_name = comp.pins[pin_name].net_name
                port_name = "{}_{}_{}".format(refdes, pin_name, net_name)
                self.port_list.append([refdes, pin_name, jedec_sname, signal_index, net_name, port_name])
                if first_dram:
                    controller_net_list.append([signal_type, signal_index, net_name])
                    port_index = port_index + 1

            # Command and address signals
            signal_type = "CA"
            signal_index_prefix = signal_type+"_"
            signal_index = 0
            for jedec_sname, pin_name in data[signal_type].items():
                net_name = comp.pins[pin_name].net_name
                port_name = "{}_{}_{}".format(refdes, pin_name, net_name)
                signal_type = signal_type.split("_")[0]
                self.port_list.append([refdes, pin_name, signal_type, signal_index, net_name, port_name])
                if first_dram:
                    controller_net_list.append([signal_type, signal_index, net_name])
                    port_index = port_index + 1
                signal_index = signal_index + 1

            # data signals
            for name in dq_group_name:
                if name in data:
                    signal_type = name
                    for jedec_sname, pin_name in data[signal_type].items():
                        net_name = comp.pins[pin_name].net_name
                        if net_name == "DUMMY":
                            continue
                        port_name = "{}_{}_{}".format(refdes, pin_name, net_name)
                        signal_type = signal_type.split("_")[0]
                        self.port_list.append([refdes, pin_name, signal_type, dq_signal_index, net_name, port_name])
                        controller_net_list.append([signal_type, dq_signal_index, net_name])
                        port_index = port_index + 1
                        dq_signal_index = dq_signal_index + 1

            # Data stroke signals
            for name in dqs_group_name:
                if name in data:
                    signal_type = name
                    t_flag = True
                    for jedec_sname, pin_name in data[signal_type].items():
                        net_name = comp.pins[pin_name].net_name
                        if net_name == "DUMMY":
                            continue
                        port_name = "{}_{}_{}".format(refdes, pin_name, net_name)
                        if t_flag:
                            signal_index = dqs_t_signal_index
                            dqs_t_signal_index = dqs_t_signal_index + 1
                            t_flag = False
                        else:
                            signal_index = dqs_c_signal_index
                            dqs_c_signal_index = dqs_c_signal_index + 1
                        self.port_list.append([refdes, pin_name, jedec_sname, signal_index, net_name, port_name])
                        controller_net_list.append([jedec_sname, signal_index, net_name])
                        port_index = port_index + 1

            first_dram = False

        # Fine port on controller
        refdes = controller_refdes
        for signal_type, signal_index, net_name in controller_net_list:
            comp = self.edbapp.core_components.components[refdes]

            pin_name = ""
            for _pin_name, obj in comp.pins.items():
                if obj.net_name == net_name:
                    pin_name = _pin_name
                    break
                else:
                    pin_name = ""

            if not pin_name:
                print("warning", net_name)
                break
            port_name = "{}_{}_{}".format(refdes, pin_name, net_name)
            self.port_list.append([refdes, pin_name, signal_type, signal_index, net_name, port_name])
            port_index = port_index + 1

        ###############################################################################################
        # Place ports

        for refdes, pin_name, signal_type, signal_index, net_name, port_name in self.port_list:
            print(port_name)
            port_name = correct_port_name(port_name)
            self.edbapp.core_siwave.create_circuit_port_on_net(refdes, net_name, refdes, self.GND_NET_NAME,
                                                               port_name=port_name)


    def save_edb_as(self, fpath_edb):
        ###############################################################################################
        # Save configured edb

        self.edbapp.save_edb_as(fpath_edb)
        self.edbapp.close_edb()

    def export_ads_cfg_file(self, fpath_ads):
        ###############################################################################################
        # Save port config to .csv file
        header = ["refdes", "pin_name", "signal_type", "signal_index", "net_name", "port_name"]
        with open(fpath_ads, "w", newline="") as f:
            writer = csv.writer((f))
            writer.writerow(header)
            writer.writerows(self.port_list)
