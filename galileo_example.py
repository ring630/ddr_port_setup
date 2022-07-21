import os
import shutil
import tempfile
from pyaedt import generate_unique_name, examples

if "PYCHARM_HOSTED" in os.environ:
    from utils.ddr_port_setup import DDRPortSetup
else:
    from .utils.ddr_port_setup import DDRPortSetup

###############################################################################
# Download file
# ~~~~~~~~~~~~~
# Download the AEDB file and copy it in the temporary folder.


tmpfold = tempfile.gettempdir()
temp_folder = os.path.join(tmpfold, generate_unique_name("Example"))
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)
example_path = examples.download_aedb()
targetfolder = os.path.join(temp_folder, "Galileo.aedb")
if os.path.exists(targetfolder):
    shutil.rmtree(targetfolder)
shutil.copytree(example_path[:-8], targetfolder)
targetfile = os.path.join(targetfolder)

print(targetfile)

###############################################################################

app = DDRPortSetup(edb_fpath=targetfile,
                       controller_refdes="U2A5",
                       dram_refdes=["U1A1", "U1B5"],
                       dram_type="ddr3_x8",
                       save_edb_as_fname=r"result_project\Galileo_new.aedb"
                       )