# Introduction
## Problem
A DDR DRAM interface can have dozens of signals. In SIwave native environment, port setup relies on net name which can 
be from design to design. It is trivial to setup SYZ extraction for DDR application. 
of ports. 
## Solution
DDR DRAM pinout is defined by JEDEC. Standard Pinout can be used to place ports without the knowledge of net names.
## What does this script do
The user only need to tell the refdes of controller and DDR DRAMs, and specify DRAM type (for example, ddr3_x8). The
script places ports on controller and DRAMs automatically.
## How to use
 