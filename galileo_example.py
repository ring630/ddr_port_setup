from utils.ddr_port_setup import DDRPortSetup
from utils.galileo_example import get_galileo_exmaple_board

targetfile = get_galileo_exmaple_board()

app = DDRPortSetup(edb_fpath=targetfile,
                   controller_refdes="U2A5",
                   dram_refdes=["U1A1", "U1B5"],
                   dram_type="ddr3_x8",
                   )
app.save_edb_as(r"result_project\Galileo_new.aedb")
app.export_ads_cfg_file(r"result_project\Galileo_new.csv")
