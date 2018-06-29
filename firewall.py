#!/usr/bin/python3
# Add ip blocks to firewall rules
# using firewalld firewall-cmd
# Tested with Python 3 on CentOS 7
# Antti Alasalmi 2018

import os, sys

# Check if running as root
if (os.getuid() != 0):
    print("Not running as root!")
    sys.exit(1)

# Define security zone
ZONE = ""

# File containing the ip addresses
# in format of single network/mask per line
IP_FILE = ""

if (not ZONE or not IP_FILE):
    print("\nError, empty variable(s):\n\n\tZONE=" + ZONE + "\n\tIP_FILE=" + IP_FILE)
    sys.exit("\nStopping execution.\n")

# if --permanent or -p argument used with the script
# use --permanent or -p to make changes permanent.
if (len(sys.argv) > 1):
    ARG = sys.argv[1].rstrip()
    if (ARG != "--permanent" or ARG != "-p"):
        sys.exit("\nError: invalid argument(s).\nArgument given: " + ARG)
    if (ARG == "-p"):
        ARG = "--permanent"
else:
    ARG = ""

# Try reading the file and start inputting commands
try:
    lines = 0
    with open(IP_FILE, "r") as reader:
        ADDRS = reader.readlines()
    for x in ADDRS:
        # Don't read comment lines
        if ("#" not in x):
            os.system("firewall-cmd --zone=" + ZONE + " --add-source=" + x.rstrip() + " " +  ARG);
            # Uncomment the next line to see progress/command.
            #print("firewall-cmd --zone=" + ZONE + " --add-source=" + x.rstrip() + " " + ARG)
            lines += 1
    print ("Found", lines, "ip addresses to add.")
# File not found
except IOError as e:
    print("File not found or other IO error,", e)
# Something else went wrong.
except Exception as e:
    print("Something went wrong:",e)
