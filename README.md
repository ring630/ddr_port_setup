# 1 Quick Start
[How to run python script in spyder](https://github.com/ring630/Material_Characterization/blob/main/docs/HOW_TO_RUN_PYAEDT_IN_SPYDER.md)

# 2 Introduction
## 2.1 Problem
A DDR DRAM interface can have dozens of signals. In SIwave native environment, port setup relies on net name which can 
be from design to design. It is trivial to setup SYZ extraction for DDR application. 
of ports. 
## 2.2 Solution
DDR DRAM pinout is defined by JEDEC. Standard Pinout can be used to place ports without the knowledge of net names.
## 2.3 What does this script do
The user only need to tell the refdes of controller and DDR DRAMs, and specify DRAM type (for example, ddr3_x8). The
script places ports on controller and DRAMs automatically.

Currently, the supported DRAM types are

1, DDR3 x8

2, DDR5 x16
## 2.4 How to use
1, Downlaod and unzip released version.

2, Open gelileo_exmaple.py in IDE. For example, Pycharm or Spyder.

3, Modify method input variables accordingly. Below is an example.

Board Galileo.aedb

controller U2A5

DRAM U1A1 U1B5
```python
app = DDRPortSetup(
   edb_fpath="Galileo.aedb",
   controller_refdes="U2A5",
   dram_refdes=["U1A1", "U1B5"],
   dram_type="ddr3_x8",
   save_edb_as_fname=r"Galileo_new.aedb"
   )
```
Configured design is saved as Galileo_new.aedb.

Import it into SIwave

<img width="1072" alt="image" src="https://user-images.githubusercontent.com/27995305/180188430-b28e30e8-fbb1-4cce-831e-97e30c8e4d4f.png">

