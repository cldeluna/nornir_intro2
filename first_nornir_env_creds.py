#!/usr/bin/python -tt
# Project: nornir_intro2
# Filename: first_nornir_env_creds
# claudia
# PyCharm


__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "8/6/20"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import os
import getpass
import warnings
# This disables warnings
# InsecureRequestWarning: Unverified HTTPS request is being made to host 'sbx-nxos-mgmt.cisco.com'
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
from nornir import InitNornir
# from nornir_netmiko.tasks import netmiko_send_command
# Updated to new Plugin module format
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get

# nornir will pick up NAPALM_USERNAME and NAPALM_PASSWORD environment variable
# export NETUSER=cisco
# export NETPASS=cisco
# In Bash (OS-X or Linux), use unset to remove an environment variable
# unset NETUSER
# unset NETPASS

def set_env(desc="Username", debug=True):
    """
    This script sets an environment variable with a name provided via the CLI and the value provided by the CLI.
    No validation checking is done.
    This is the Python equivalent of executing an export command in your systems BASH (or other CLI) shell
    export NETPASS=cisco
    :param desc: Cosmetic note used to provide a hint in the input statement as to what this environment
    variable is. Defaults to "Username"
    :param debug:  Boolean optional parameter. When set to True, the function will print output to STDOut.
    :return:
    """
    env_var = input(f"\nPlease enter {desc} environment variable name:\n")
    env_var_value = input(f"Please enter {desc} environment variable value:\n")

    os.environ[env_var] = env_var_value

    if debug:
        print(f'{env_var}={os.environ[env_var]} environment variable has been set.\n')


def set_creds(self, prefix="ENVVAR", context="default"):
    """ Check for username and password env vars first.  If those
    don't exist, then prompt user for creds and set the values in Nornir, in the appropriate context
    This function is specific to setting username and password with names in a specific format.
    CREDIT: Chris Crook ([@ctopher78](https://twitter.com/ctopher78)) Posted to Nornir Slack Channel Oct 18, 2019
    Note: "self" is the Nornir object for which we are setting credentials
    The context will define the object level:
    - default = Default Nornir password for all
    - group = Password set for Nornir group (at the group level)
    - device = Password set for a specific device

    For group and device environment variables should be set in the format:
    <Uppercase group or device name>_USR
    <Uppercase group or device name>_PWD

    """
    # Set boolean values to False
    # These will be used to determine if the specified environment variables are already set
    username_is_set = False
    password_is_set = False

    # Define the environment variable names we will search for
    if context=="default":
        # These default environment variable names are arbitrary
        usr = "NETUSER"
        pwd = "NETPASS"
        if self.inventory.defaults.username:
            username_is_set = True
        if self.inventory.defaults.password:
            password_is_set = True

    else:
        usr = f"{prefix.upper()}_USR"
        pwd = f"{prefix.upper()}_PWD"

        # Set booleans to True if the object passed into the function has username and password already set
        if self.username:
            username_is_set = True
        if self.password:
            password_is_set = True

    # Try to get the username and password variables from the environment (see if they are set)
    username = os.environ.get(usr)
    password = os.environ.get(pwd)

    # Print current environment variables
    # print(os.environ)

    print(f"\n============= Setting Credentials for {self} with context {context} =============")
    print(f"Username from env var is: {username}")
    print(f"Password from env var is: {password}\n")

    # If username (from environment variable) and username_is set are both False, that means that the
    # environment variable is not set nor is the username set (say via the groups.yaml file) so the topology
    # currently has no username to use on devices in this context.
    # Lets request the username from the command line
    # Note:  The username is not set as an environment variable but rather the appropriate Nornir context values are set
    if not username and not username_is_set:
        uname = input(
            f"\nPlease enter username (or set `export {usr}=<your_username>` to avoid this message): "
        )
        username = uname
    else:
        print(f"\n\tUsername set via environmental variable {usr} ")

    # Prompt for password (as with username) using the same logic.
    if not password and not password_is_set:
        pwd = getpass.getpass(
            f"\nPlease enter password (or set `export {pwd}=<your_password>` to avoid this message): "
        )
        password = pwd

    else:
        print(f"\n\tPassword set via environmental variable {pwd} ")

    # Set the Nornir values in the appropriate context
    if context=="default":
        self.inventory.defaults.username = username
        self.inventory.defaults.password = password
    else:
        self.username = username
        self.password = password


def main():

    nr = InitNornir(config_file='config.yaml')

    # For Windows systems, set the env variables within the scope of the script
    # This is executed when the script is run with the -s option
    if arguments.set_envs:
        set_env(desc="Username")
        set_env(desc="Password")

    # This function will check to make sure credentials have been set either via environment variables or via
    # the topology YAML files.
    set_creds(nr)
    # print(dir(nr))
    print("Hosts derived from the Inventory file are: \t{}".format(nr.inventory.hosts))
    print("Groups derived from the Inventory file are: \t{}".format(nr.inventory.groups))

    print("\nDecomposing Groups...")
    my_groups = nr.inventory.groups
    group_keys = list(my_groups.keys())
    print("Group keys = {} of type {} ".format(group_keys, type(group_keys)))
    for i in group_keys:
        # print(f"- {i}")
        # print(f"dir of {i} is {dir(my_groups[i])}")
        # print(f'is username set {my_groups[i].username}')
        # print(f'is password set {my_groups[i].password}')
        if not my_groups[i].username or not my_groups[i].password:
            set_creds(my_groups[i], prefix=i, context="group")
            # export UWACO_NETWORK_USR=cisco
            # export UWACO_NETWORK_PWD=cisco

    print("\nDecomposing Hosts...")
    my_hosts = nr.inventory.hosts
    print("Type of nr.inventory.hosts in var my_hosts is {}".format(type(my_hosts)))

    host_keys = list(my_hosts.keys())
    print("Host keys = {} of type {} ".format(host_keys, type(host_keys)))
    for i in host_keys:
        # print(f"- {i}")
        # print(f"dir of {i} is {dir(my_hosts[i])}")
        if not my_hosts[i].username:
            set_creds(my_hosts[i], prefix=i, context="device")
            # devnet_sandbox_iosxe
            # export DEVNET_SANDBOX_IOSXE_USR=cisco
            # export DEVNET_SANDBOX_IOSXE=cisco

    print("\n")

    print(f"Logging into hosts in inventory and getting napalm facts...")
    result = nr.run(
        napalm_get,
        getters=['get_facts'])

    print(f"napalm facts stored in the variable 'result'...{result}")
    # Printing now may help you decompose the resulting objects
    print_result(result)


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python env_creds' ")

    parser.add_argument('-s', '--set_envs', action='store_true', default=False, help='When True, script will prompt for '
                                                                                     'Username and Password to set as '
                                                                                     'Environment Variables')

    arguments = parser.parse_args()
    main()
