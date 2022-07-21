import os
import json
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
    PORT_LIST = []

    def __init__(self,
                 edb_fpath,
                 controller_refdes,
                 dram_refdes,
                 dram_type,
                 save_edb_as_fname=None,
                 ):

        if not isinstance(dram_refdes, list):
            dram_refdes = [dram_refdes]

        with open(os.path.join("_ddrx_pin_mapping", self.DRAM_TYPE_LIST[dram_type]), encoding="utf-8") as f:
            data = json.load(f)

        self.edbapp = Edb(edbpath=edb_fpath, edbversion=self.EDB_VERSION)

        ###############################################################################################
        # Find ports on DRAMs
        dq_group_name = ["dq", "ldq", "udq"]
        dqs_group_name = ["dqs", "ldqs", "udqs"]

        controller_net_list = []  # jedec_sname net_name
        port_list = []  # refdes pin_name net_name port_name
        port_index = 0
        first_dram = True
        for refdes in dram_refdes:
            comp = self.edbapp.core_components.components[refdes]

            # clock signals
            for jedec_sname, pin_name in data["ck"].items():
                net_name = comp.pins[pin_name].net_name
                port_name = "{}_{}_{}_{}".format(port_index, refdes, jedec_sname, net_name)
                port_list.append([refdes, pin_name, net_name, port_name])
                if first_dram:
                    controller_net_list.append([jedec_sname, net_name])
                port_index = port_index + 1

            # Command and address signals
            for jedec_sname, pin_name in data["ca"].items():
                net_name = comp.pins[pin_name].net_name
                port_name = "{}_{}_{}_{}".format(port_index, refdes, jedec_sname, net_name)
                port_list.append([refdes, pin_name, net_name, port_name])
                if first_dram:
                    controller_net_list.append([jedec_sname, net_name])
                port_index = port_index + 1

            # data signals
            for name in dq_group_name:
                if name in data:
                    for jedec_sname, pin_name in data[name].items():
                        net_name = comp.pins[pin_name].net_name
                        if net_name == "DUMMY":
                            continue
                        port_name = "{}_{}_{}_{}".format(port_index, refdes, jedec_sname, net_name)
                        port_list.append([refdes, pin_name, net_name, port_name])
                        controller_net_list.append([jedec_sname, net_name])
                        port_index = port_index + 1

            # Data stroke signals
            for name in dqs_group_name:
                if name in data:
                    for jedec_sname, pin_name in data[name].items():
                        net_name = comp.pins[pin_name].net_name
                        if net_name == "DUMMY":
                            continue
                        port_name = "{}_{}_{}_{}".format(port_index, refdes, jedec_sname, net_name)
                        port_list.append([refdes, pin_name, net_name, port_name])
                        controller_net_list.append([jedec_sname, net_name])
                        port_index = port_index + 1

            first_dram = False

        # Fine port on controller
        for jedec_sname, net_name in controller_net_list:
            comp = self.edbapp.core_components.components[controller_refdes]

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
            port_name = "{}_{}_{}_{}".format(port_index, controller_refdes, jedec_sname, net_name)
            port_list.append([controller_refdes, pin_name, net_name, port_name])
            port_index = port_index + 1

        ###############################################################################################
        # Place ports
        for refdes, pin_name, net_name, port_name in port_list:
            print(refdes, pin_name, net_name, port_name)
            port_name = correct_port_name(port_name)
            self.edbapp.core_siwave.create_circuit_port_on_net(refdes, net_name, refdes, self.GND_NET_NAME,
                                                               port_name=port_name)

        ###############################################################################################
        # Save configured edb
        if not save_edb_as_fname:
            save_edb_as_fname = edb_fpath.replace(".aedb", "_w_ports.aedb")

        self.edbapp.save_edb_as(save_edb_as_fname)
        self.edbapp.close_edb()
