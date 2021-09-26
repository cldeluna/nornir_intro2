#!/usr/bin/python -tt
# Project: nornir_intro2
# Filename: netmiko_nornir
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "5/5/20"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import time
import warnings
# This disables warnings
# InsecureRequestWarning: Unverified HTTPS request is being made to host 'sbx-nxos-mgmt.cisco.com'
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result


def main():

    # Create instance nr using default hosts.yaml and groups.yaml
    nr = InitNornir(config_file='config.yaml')

    # The nr object will have special properties and capabilities.
    # Use dir() to see what they are. Uncomment the print line below to see the output
    # print(dir(nr))
    print("Hosts derived from the Inventory file are: \t{}".format(nr.inventory.hosts))
    print("Groups derived from the Inventory file are: \t{}".format(nr.inventory.groups))

    print("\nDecomposing Groups...")
    my_groups = nr.inventory.groups
    group_keys = list(my_groups.keys())
    print("Group keys = {} of type {} ".format(group_keys, type(group_keys)))
    for i in group_keys:
        print(f"- {i}")

    print("\nDecomposing Hosts...")
    my_hosts = nr.inventory.hosts
    print("Type of nr.inventory.hosts in var my_hosts is {}".format(type(my_hosts)))

    host_keys = list(my_hosts.keys())
    print("Host keys = {} of type {} ".format(host_keys, type(host_keys)))
    for i in host_keys:
        print(f"- {i}")
    print("\n")

    show_command = 'show ip route'
    print(f"Logging into hosts in inventory and executing show command...")
    print(f"WARNING: netmiko uses ssh, but the current group.yaml sets the port for the NX-OS device to the API port."
          f"\nIf you see an ssh error in your results, edit your groups.yaml file and "
          f"\ncomment out the API port and uncomment the SSH port for the device")
    time.sleep(3)
    result = nr.run(netmiko_send_command, command_string=show_command)

    print(f"\ncommand output stored in the variable 'result'...")
    print_result(result)

    print(f"\nDecomposing Nornir Result Object of type {type(result)}...\n")
    print(result.items())
    print(result.values())
    print(result.keys())

    for k in result.keys():
        print(f"\n========= Result Keys: \n\t{k}")
        # Lets try to understand what we get back
        print(result[k])
        print(dir(result[k]))
        output = result[k][0]
        print(output)
        print(f"========= \n")

# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python netmiko_nornir' ")

    arguments = parser.parse_args()
    main()
