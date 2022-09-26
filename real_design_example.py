from utils.ddr_port_setup import DDRPortSetup

app = DDRPortSetup(edb_fpath=r"git_excluded_dir\DDR5.aedb",
                   controller_refdes="D1",
                   dram_refdes=["D11400", "D11401", "D11402"],
                   dram_type="ddr5_x16",
                   )
app.save_edb_as(r"result_project\ddr5_new.aedb")
app.export_ads_cfg_file(r"result_project\ddr5_new.csv")
