import pandas as pd
import csv


def export_ads_format(data, channel_id, output_fpath):
    # Save as ADS format
    header_ads = ["ReferenceDesignator",
                  "PinName",
                  "SignalType",
                  "SignalIndex",
                  "PortName",
                  "ChannelID",
                  "Terminated",
                  "TerminationOhms",
                  "AltSignalType",
                  "AltSignalIndex",
                  "DiePin",
                  "BallPin",
                  "IbisPin"]
    with open(output_fpath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header_ads)
        data.pop(0)
        for r in data:
            refdes, pin_name, signal_type, signal_index, net_name, port_name = r
            new_line = refdes, pin_name, signal_type, signal_index, port_name, channel_id, 0, 50
            writer.writerow(new_line)



with open(r"C:\Users\hzhou\ddr_port_setup\result_project\ddr5_new.csv") as f:
    reader = csv.reader(f)
    header = ["refdes", "pin_name", "signal_type", "signal_index", "net_name", "port_name"]
    data = []
    for l in reader:
        if len(l):
            data.append(l)

    export_ads_format(data, "A2", r"C:\Users\hzhou\ddr_port_setup\result_project\ddr5_ads.csv")
