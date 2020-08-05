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
import argparse

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result


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

    result = nr.run(netmiko_send_command, command_string=show_command)

    print(f"command output stored in the variable 'result'...")

    # Printing now may help you decompose the resulting objects
    # print(result)
    # print(dir(result))
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

    #parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    parser.add_argument('-a', '--all', help='Execute all exercises in week 4 assignment', action='store_true',
                        default=False)
    arguments = parser.parse_args()
    main()
