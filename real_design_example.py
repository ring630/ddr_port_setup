from utils.ddr_port_setup import DDRPortSetup

from utils.example_board import ExampleBoard

eboard = ExampleBoard()


app = DDRPortSetup(edb_fpath=eboard.nokia_huge_board)
app.setup_ports(controller_refdes="D190000",
                dram_refdes=["D195003", "D195000", "D195001", "D195002"],
                dram_type="ddr4_x16",
                )

"""
app = DDRPortSetup(edb_fpath=eboard.intel_galileo)
app.setup_ports(controller_refdes="U2A5",
                dram_refdes=["U1A1", "U1B5"],
                dram_type="ddr3_x8",
                )
"""
app.save_edb_to_temp_folder()
