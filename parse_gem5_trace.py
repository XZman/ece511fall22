#!/usr/bin/env python3

import math
import argparse

# Parse the gem5 trace file and output a DRAMsim3 trace file

# parse args
parser = argparse.ArgumentParser(description='Parse gem5 trace file and output a DRAMsim3 trace file')

parser.add_argument('--gem5_trace_file', type=str, required=True, help='gem5 trace file (input)')
parser.add_argument('--dramsim3_trace_file', type=str, required=True, help='DRAMsim3 trace file (output)')

parser.add_argument('--dramsim3_tCK', type=float, default=1.25, help='DRAMsim3 tCK (ns) (default: 1.25)')
parser.add_argument('--gem5_tick_per_second', type=int, default=1000000000000, help='gem5 tick per second (default: 1e12)')

args = parser.parse_args()

dramsim3_freq = 1e9 / args.dramsim3_tCK

with open(args.gem5_trace_file, "r") as fin:
    with open(args.dramsim3_trace_file, "w") as fout:
        for line in fin:
            tokens = line.strip().split()
            assert len(tokens) == 3, line
            # convert clock domain from gem5 to dramsim3 for the given tCK
            tick = math.ceil(int(tokens[2]) * dramsim3_freq / args.gem5_tick_per_second)
            out_str = f"{tokens[0]} {tokens[1]} {tick}\n"
            fout.write(out_str)
        print(f"final tick: {tick}")
