# First Nornir (formerly brigade) Test Run
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/cldeluna/nornir_intro2)

## Summary

This repository accompanies my post [Nornir – A New Network Automation Framework](https://gratuitous-arp.net/nornir-a-new-network-automation-framework/) and is my first test of the network automation framework formerly known as brigade (and now known as [Nornir](https://pypi.org/project/nornir/) - not responsible for alliteration!) but updated for the latest version.

This was my first use of Nornir so the code has lots of comments as I figured stuff out.  I started out with the sample get facts *run\_nornir.py* script from from [Patrick Ogenstad at Networklore.](https://networklore.com/introducing-brigade/)

I'm fairly excited about this!  It took me about 45 minutes to get things set up on my Windows 10 system.  It took almost no time at all on my Mac.

Using PyCharm on my mac the **print_result** output is formatted and color coded nicely.  Using PyCharm on my Windows 10 system the output is less colorful.

The ***first\_nornir.py*** script is my attempt to take the basics from [Mr. Ogenstad's example script](https://networklore.com/introducing-brigade/) and decompose the objects and resulting data structures.  It took me a while the first time and with Nornir2 it took me even longer!  It makes complete sense and these objects are highly flexible but for someone newish to Python it nearly made my head explode.  Luckily, with cranium still intact, I'm still very excited about this framework!   

Having said that, if you are not comfortable with some of these more complex data structures please see [Decomposing Data Structures](https://gratuitous-arp.net/decomposing-complex-json-data-structures/) or sign up for one of [Kirk Byers](https://pynet.twb-tech.com/) Python for Network Engineers courses!

My next Sunday afternoon project will involve [generating configurations and applying them](https://gratuitous-arp.net/configuration-creation-with-nornir/).



## Installation

1. [Define a nornir virtual environment with Python3](https://realpython.com/python-virtual-environments-a-primer/).
2. Activate your new virtual environment
3. Install all the required modules with the pip install command as shown below

```
pip install -r requirements.txt
```



## Code Example

Like Ansible, Nornir will leverage inventory information.  Here you see a very basic **groups.yaml** file which can also contain a default section for more general values and a **hosts.yaml** file which can reference specific or more general group settings defined in the groups.yaml file.  These files can take any **key:value** pair and the values with the "nornir_" prefix have special meaning as you would expect.

### Files that set up your environment and devices

Note: The scripts in the repository comment out local devices and retain the [DevNet](https://developer.cisco.com/) Always On IOS-XE and NX-OS devices so that the scripts can be run immediately with results (unless DevNet is undergoing maintenance).  Local devices are left in for example purposes only.  The output shown below includes output from local devices.

###### groups.yaml

```
  ---
# DevNet Always On Sandbox Devices
devnet_sandbox_iosxe:
  platform: ios
  port: 8181
  username: root
  password: D_Vay!_10&
#
devnet_sandbox_nxos:
  platform: nxos
  # For use with Netmiko script. Uncomment port 8181 and comment out port 443 (used for NXOS API)
  # port: 8181
  # For use with first Nornir (napalm getter) script which uses NXOS API to communicate with NXOS platforms
  port: 443
  username: admin
  password: Admin_1234!

```

###### hosts.yaml

     ---
    # DevNet Always On Sandbox Devices
    ios-xe-mgmt:
      hostname: ios-xe-mgmt.cisco.com
      groups: ['devnet_sandbox_iosxe']
     
    sbx-nxos-mgmt:
      hostname: sbx-nxos-mgmt.cisco.com
      groups: ['devnet_sandbox_nxos']



#### Scripts in the Repository

| Script                    |                                                              |
| ------------------------- | ------------------------------------------------------------ |
| run\_nornir.py            | Sample nornir script using napalm get facts from from Patrick Ogenstad at Networklore |
| first\_nornir.py          | Building on Patrick Ogenstad run_nornir.py script, this script works through understanding the returned objects and structured data. |
| netmiko_nornir.py         | Now that we are little familiar with the basics of Nornir, let's use Nornir with Netmiko to get the output of specific commands rather than the structured data returned by Napalm facts.<br />Make sure to update the NXOS sandbox in the groups.yaml file to use port 8181. |
| first_nornir_env_creds.py | This script is basically a copy of first_nornir.py but showing how environment variables can be used instead of hardcoding the credentials into the groups.yaml file.  Many thanks to Chris Crook ([@ctopher78](https://twitter.com/ctopher78)) for getting it started.  For a full discussion of this new credentials strategy see [How Network Engineers Can Manage Credentials and Keys More Securely in Python](https://gratuitous-arp.net/managing-credentials-and-keys-more-securely-in-python-for-network-engineers/) |

#### first_nornir.py

The first part of the **first_nornir.py** script initializes a nornir object called **nr**.  This reads in the topology and host information and the script shows how to get to some of that information.

Next, we use the run method on the nr object..well..to run some commands which in this case uses napalm to get facts.

The next sections of the script attempt to deconstruct the objects into workable values like getting the keys of all the hosts.

##### Typical script execution output

```
(nornir2) Claudias-iMac:nornir_intro2 claudia$ python first_nornir.py 
Hosts derived from the Inventory file are:      {'eu-med-as01': Host: eu-med-as01, 'arctic-ds01-as01': Host: arctic-ds01-as01}
Groups derived from the Inventory file are:     {'uwaco_network': Group: uwaco_network}

Decomposing Groups...
Group keys = ['uwaco_network'] of type <class 'list'> 
- uwaco_network

Decomposing Hosts...
Type of nr.inventory.hosts in var my_hosts is <class 'nornir.core.inventory.Hosts'>
Host keys = ['eu-med-as01', 'arctic-ds01-as01'] of type <class 'list'> 
- eu-med-as01
- arctic-ds01-as01



Logging into hosts in inventory and getting napalm facts...
napalm facts stored in the varialbe 'result'...

Decomposing Nornir Result Object of type <class 'nornir.core.task.AggregatedResult'>...

Iterating through result object of type<class 'nornir.core.task.MultiResult'> for item eu-med-as01
        Get the top level key(s) for the device:
        dict_keys(['get_facts'])

        Get the next level of key(s):
        dict_keys(['uptime', 'vendor', 'os_version', 'serial_number', 'model', 'hostname', 'fqdn', 'interface_list'])
        Decomposing Result Object for hostname eu-med-as01...
                Key uptime       has Value: 21900
                Key vendor       has Value: Cisco
                Key os_version   has Value: Catalyst L3 Switch Software (CAT3K_CAA-UNIVERSALK9-M), Version 16.6.2, RELEASE SOFTWARE (fc2)
                Key serial_number        has Value: FOC1706X0QR
                Key model        has Value: WS-C3850-24P
                Key hostname     has Value: eu-med-as01
                Key fqdn         has Value: eu-med-as01.uwaco.net
                Key interface_list       has Value: ['Vlan1', 'Vlan10', 'Vlan11', 'Vlan12', 'Vlan100', 'Vlan101', 'Vlan102', 'Vlan103', 'Vlan104', 'Vlan105', 'Vlan106', 'Vlan107', 'Vlan108', 'Vlan109', 'Vlan110', 'Vlan111', 'Vlan112', 'Vlan114', 'Vlan115', 'Vlan116', 'Vlan117', 'Vlan118', 'Vlan120', 'Vlan122', 'Vlan123', 'Vlan124', 'Vlan125', 'Vlan126', 'Vlan128', 'Vlan131', 'Vlan136', 'Vlan137', 'Vlan138', 'Vlan139', 'Vlan140', 'Vlan188', 'Vlan200', 'Vlan201', 'Vlan202', 'Vlan203', 'Vlan204', 'Vlan205', 'Vlan206', 'Vlan207', 'Vlan208', 'Vlan209', 'Vlan210', 'Vlan211', 'Vlan212', 'Vlan213', 'Vlan214', 'Vlan215', 'Vlan216', 'Vlan217', 'Vlan218', 'Vlan220', 'Vlan222', 'Vlan223', 'Vlan228', 'Vlan236', 'Vlan240', 'Vlan600', 'Vlan601', 'Vlan602', 'Vlan700', 'Vlan701', 'Vlan800', 'GigabitEthernet0/0', 'GigabitEthernet1/0/1', 'GigabitEthernet1/0/2', 'GigabitEthernet1/0/3', 'GigabitEthernet1/0/4', 'GigabitEthernet1/0/5', 'GigabitEthernet1/0/6', 'GigabitEthernet1/0/7', 'GigabitEthernet1/0/8', 'GigabitEthernet1/0/9', 'GigabitEthernet1/0/10', 'GigabitEthernet1/0/11', 'GigabitEthernet1/0/12', 'GigabitEthernet1/0/13', 'GigabitEthernet1/0/14', 'GigabitEthernet1/0/15', 'GigabitEthernet1/0/16', 'GigabitEthernet1/0/17', 'GigabitEthernet1/0/18', 'GigabitEthernet1/0/19', 'GigabitEthernet1/0/20', 'GigabitEthernet1/0/21', 'GigabitEthernet1/0/22', 'GigabitEthernet1/0/23', 'GigabitEthernet1/0/24', 'GigabitEthernet1/1/1', 'GigabitEthernet1/1/2', 'GigabitEthernet1/1/3', 'GigabitEthernet1/1/4', 'Te1/1/1', 'Te1/1/2', 'Te1/1/3', 'Te1/1/4', 'GigabitEthernet2/0/1', 'GigabitEthernet2/0/2', 'GigabitEthernet2/0/3', 'GigabitEthernet2/0/4', 'GigabitEthernet2/0/5', 'GigabitEthernet2/0/6', 'GigabitEthernet2/0/7', 'GigabitEthernet2/0/8', 'GigabitEthernet2/0/9', 'GigabitEthernet2/0/10', 'GigabitEthernet2/0/11', 'GigabitEthernet2/0/12', 'GigabitEthernet2/0/13', 'GigabitEthernet2/0/14', 'GigabitEthernet2/0/15', 'GigabitEthernet2/0/16', 'GigabitEthernet2/0/17', 'GigabitEthernet2/0/18', 'GigabitEthernet2/0/19', 'GigabitEthernet2/0/20', 'GigabitEthernet2/0/21', 'GigabitEthernet2/0/22', 'GigabitEthernet2/0/23', 'GigabitEthernet2/0/24', 'GigabitEthernet2/1/1', 'GigabitEthernet2/1/2', 'GigabitEthernet2/1/3', 'GigabitEthernet2/1/4', 'Te2/1/1', 'Te2/1/2', 'Te2/1/3', 'Te2/1/4', 'GigabitEthernet3/0/1', 'GigabitEthernet3/0/2', 'GigabitEthernet3/0/3', 'GigabitEthernet3/0/4', 'GigabitEthernet3/0/5', 'GigabitEthernet3/0/6', 'GigabitEthernet3/0/7', 'GigabitEthernet3/0/8', 'GigabitEthernet3/0/9', 'GigabitEthernet3/0/10', 'GigabitEthernet3/0/11', 'GigabitEthernet3/0/12', 'GigabitEthernet3/0/13', 'GigabitEthernet3/0/14', 'GigabitEthernet3/0/15', 'GigabitEthernet3/0/16', 'GigabitEthernet3/0/17', 'GigabitEthernet3/0/18', 'GigabitEthernet3/0/19', 'GigabitEthernet3/0/20', 'GigabitEthernet3/0/21', 'GigabitEthernet3/0/22', 'GigabitEthernet3/0/23', 'GigabitEthernet3/0/24', 'GigabitEthernet3/1/1', 'GigabitEthernet3/1/2', 'GigabitEthernet3/1/3', 'GigabitEthernet3/1/4', 'Te3/1/1', 'Te3/1/2', 'Te3/1/3', 'Te3/1/4', 'GigabitEthernet4/0/1', 'GigabitEthernet4/0/2', 'GigabitEthernet4/0/3', 'GigabitEthernet4/0/4', 'GigabitEthernet4/0/5', 'GigabitEthernet4/0/6', 'GigabitEthernet4/0/7', 'GigabitEthernet4/0/8', 'GigabitEthernet4/0/9', 'GigabitEthernet4/0/10', 'GigabitEthernet4/0/11', 'GigabitEthernet4/0/12', 'GigabitEthernet4/0/13', 'GigabitEthernet4/0/14', 'GigabitEthernet4/0/15', 'GigabitEthernet4/0/16', 'GigabitEthernet4/0/17', 'GigabitEthernet4/0/18', 'GigabitEthernet4/0/19', 'GigabitEthernet4/0/20', 'GigabitEthernet4/0/21', 'GigabitEthernet4/0/22', 'GigabitEthernet4/0/23', 'GigabitEthernet4/0/24', 'GigabitEthernet4/1/1', 'GigabitEthernet4/1/2', 'GigabitEthernet4/1/3', 'GigabitEthernet4/1/4', 'Te4/1/1', 'Te4/1/2', 'Te4/1/3', 'Te4/1/4', 'GigabitEthernet5/0/1', 'GigabitEthernet5/0/2', 'GigabitEthernet5/0/3', 'GigabitEthernet5/0/4', 'GigabitEthernet5/0/5', 'GigabitEthernet5/0/6', 'GigabitEthernet5/0/7', 'GigabitEthernet5/0/8', 'GigabitEthernet5/0/9', 'GigabitEthernet5/0/10', 'GigabitEthernet5/0/11', 'GigabitEthernet5/0/12', 'GigabitEthernet5/0/13', 'GigabitEthernet5/0/14', 'GigabitEthernet5/0/15', 'GigabitEthernet5/0/16', 'GigabitEthernet5/0/17', 'GigabitEthernet5/0/18', 'GigabitEthernet5/0/19', 'GigabitEthernet5/0/20', 'GigabitEthernet5/0/21', 'GigabitEthernet5/0/22', 'GigabitEthernet5/0/23', 'GigabitEthernet5/0/24', 'GigabitEthernet5/1/1', 'GigabitEthernet5/1/2', 'GigabitEthernet5/1/3', 'GigabitEthernet5/1/4', 'Te5/1/1', 'Te5/1/2', 'Te5/1/3', 'Te5/1/4', 'GigabitEthernet6/0/1', 'GigabitEthernet6/0/2', 'GigabitEthernet6/0/3', 'GigabitEthernet6/0/4', 'GigabitEthernet6/0/5', 'GigabitEthernet6/0/6', 'GigabitEthernet6/0/7', 'GigabitEthernet6/0/8', 'GigabitEthernet6/0/9', 'GigabitEthernet6/0/10', 'GigabitEthernet6/0/11', 'GigabitEthernet6/0/12', 'GigabitEthernet6/0/13', 'GigabitEthernet6/0/14', 'GigabitEthernet6/0/15', 'GigabitEthernet6/0/16', 'GigabitEthernet6/0/17', 'GigabitEthernet6/0/18', 'GigabitEthernet6/0/19', 'GigabitEthernet6/0/20', 'GigabitEthernet6/0/21', 'GigabitEthernet6/0/22', 'GigabitEthernet6/0/23', 'GigabitEthernet6/0/24', 'GigabitEthernet6/1/1', 'GigabitEthernet6/1/2', 'GigabitEthernet6/1/3', 'GigabitEthernet6/1/4', 'Te6/1/1', 'Te6/1/2', 'Te6/1/3', 'Te6/1/4']


Iterating through result object of type<class 'nornir.core.task.MultiResult'> for item arctic-ds01-as01
        Get the top level key(s) for the device:
        dict_keys(['get_facts'])

        Get the next level of key(s):
        dict_keys(['uptime', 'vendor', 'os_version', 'serial_number', 'model', 'hostname', 'fqdn', 'interface_list'])
        Decomposing Result Object for hostname arctic-ds01-as01...
                Key uptime       has Value: 10140
                Key vendor       has Value: Cisco
                Key os_version   has Value: C3750 Software (C3750-IPSERVICESK9-M), Version 12.2(55)SE3, RELEASE SOFTWARE (fc1)
                Key serial_number        has Value: CAT1028NM3L
                Key model        has Value: WS-C3750-48TS
                Key hostname     has Value: mgmt-sw05
                Key fqdn         has Value: mgmt-sw05.uwaco.net
                Key interface_list       has Value: ['Vlan1', 'Vlan30', 'Vlan100', 'Vlan101', 'FastEthernet1/0/1', 'FastEthernet1/0/2', 'FastEthernet1/0/3', 'FastEthernet1/0/4', 'FastEthernet1/0/5', 'FastEthernet1/0/6', 'FastEthernet1/0/7', 'FastEthernet1/0/8', 'FastEthernet1/0/9', 'FastEthernet1/0/10', 'FastEthernet1/0/11', 'FastEthernet1/0/12', 'FastEthernet1/0/13', 'FastEthernet1/0/14', 'FastEthernet1/0/15', 'FastEthernet1/0/16', 'FastEthernet1/0/17', 'FastEthernet1/0/18', 'FastEthernet1/0/19', 'FastEthernet1/0/20', 'FastEthernet1/0/21', 'FastEthernet1/0/22', 'FastEthernet1/0/23', 'FastEthernet1/0/24', 'FastEthernet1/0/25', 'FastEthernet1/0/26', 'FastEthernet1/0/27', 'FastEthernet1/0/28', 'FastEthernet1/0/29', 'FastEthernet1/0/30', 'FastEthernet1/0/31', 'FastEthernet1/0/32', 'FastEthernet1/0/33', 'FastEthernet1/0/34', 'FastEthernet1/0/35', 'FastEthernet1/0/36', 'FastEthernet1/0/37', 'FastEthernet1/0/38', 'FastEthernet1/0/39', 'FastEthernet1/0/40', 'FastEthernet1/0/41', 'FastEthernet1/0/42', 'FastEthernet1/0/43', 'FastEthernet1/0/44', 'FastEthernet1/0/45', 'FastEthernet1/0/46', 'FastEthernet1/0/47', 'FastEthernet1/0/48', 'GigabitEthernet1/0/1', 'GigabitEthernet1/0/2', 'GigabitEthernet1/0/3', 'GigabitEthernet1/0/4', 'FastEthernet2/0/1', 'FastEthernet2/0/2', 'FastEthernet2/0/3', 'FastEthernet2/0/4', 'FastEthernet2/0/5', 'FastEthernet2/0/6', 'FastEthernet2/0/7', 'FastEthernet2/0/8', 'FastEthernet2/0/9', 'FastEthernet2/0/10', 'FastEthernet2/0/11', 'FastEthernet2/0/12', 'FastEthernet2/0/13', 'FastEthernet2/0/14', 'FastEthernet2/0/15', 'FastEthernet2/0/16', 'FastEthernet2/0/17', 'FastEthernet2/0/18', 'FastEthernet2/0/19', 'FastEthernet2/0/20', 'FastEthernet2/0/21', 'FastEthernet2/0/22', 'FastEthernet2/0/23', 'FastEthernet2/0/24', 'FastEthernet2/0/25', 'FastEthernet2/0/26', 'FastEthernet2/0/27', 'FastEthernet2/0/28', 'FastEthernet2/0/29', 'FastEthernet2/0/30', 'FastEthernet2/0/31', 'FastEthernet2/0/32', 'FastEthernet2/0/33', 'FastEthernet2/0/34', 'FastEthernet2/0/35', 'FastEthernet2/0/36', 'FastEthernet2/0/37', 'FastEthernet2/0/38', 'FastEthernet2/0/39', 'FastEthernet2/0/40', 'FastEthernet2/0/41', 'FastEthernet2/0/42', 'FastEthernet2/0/43', 'FastEthernet2/0/44', 'FastEthernet2/0/45', 'FastEthernet2/0/46', 'FastEthernet2/0/47', 'FastEthernet2/0/48', 'GigabitEthernet2/0/1', 'GigabitEthernet2/0/2', 'GigabitEthernet2/0/3', 'GigabitEthernet2/0/4']





```



Lastly, we use the built in **print_result** command to print the resulting output in a highly readable way.  

You may want to do this earlier because this will help you understand the data structure.

Example of the nornir **print_result** module which prints an Ansible-like status to stdout.


```
(nornir) claudia@Claudias-iMac nornir_intro2 % python first_nornir.py
Hosts derived from the Inventory file are:      {'ios-xe-mgmt': Host: ios-xe-mgmt, 'sbx-nxos-mgmt': Host: sbx-nxos-mgmt}
Groups derived from the Inventory file are:     {'devnet_sandbox_iosxe': Group: devnet_sandbox_iosxe, 'devnet_sandbox_nxos': Group: devnet_sandbox_nxos}

Decomposing Groups...
Group keys = ['devnet_sandbox_iosxe', 'devnet_sandbox_nxos'] of type <class 'list'> 
- devnet_sandbox_iosxe
- devnet_sandbox_nxos

Decomposing Hosts...
Type of nr.inventory.hosts in var my_hosts is <class 'nornir.core.inventory.Hosts'>
Host keys = ['ios-xe-mgmt', 'sbx-nxos-mgmt'] of type <class 'list'> 
- ios-xe-mgmt
- sbx-nxos-mgmt


Logging into hosts in inventory and getting napalm facts...
napalm facts stored in the variable 'result'...
napalm_get**********************************************************************
* ios-xe-mgmt ** changed : False ***********************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'get_facts': { 'fqdn': 'csr1000v.abc.inc',
                 'hostname': 'csr1000v',
                 'interface_list': [ 'GigabitEthernet1',
                                     'GigabitEthernet2',
                                     'GigabitEthernet3',
                                     'Loopback2',
                                     'Loopback10',
                                     'Loopback103',
                                     'Loopback120',
                                     'Loopback200',
                                     'VirtualPortGroup0'],
                 'model': 'CSR1000V',
                 'os_version': 'Virtual XE Software '
                               '(X86_64_LINUX_IOSD-UNIVERSALK9-M), Version '
                               '16.9.3, RELEASE SOFTWARE (fc2)',
                 'serial_number': '9XXJEG7SFU4',
                 'uptime': 49560,
                 'vendor': 'Cisco'}}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* sbx-nxos-mgmt ** changed : False *********************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'get_facts': { 'fqdn': 'sbx-n9kv-ao',
                 'hostname': 'sbx-n9kv-ao',
                 'interface_list': [ 'mgmt0',
                                     'Ethernet1/1',
                                     'Ethernet1/2',
                                     'Ethernet1/3',
                                     'Ethernet1/4',
                                     'Ethernet1/5',
                                     'Ethernet1/6',
                                     'Ethernet1/7',
                                     'Ethernet1/8',
                                     'Ethernet1/9',
                                     'Ethernet1/10',
                                     'Ethernet1/11',
                                     'Ethernet1/12',
                                     'Ethernet1/13',
                                     'Ethernet1/14',
                                     'Ethernet1/15',
                                     'Ethernet1/16',
                                     'Ethernet1/17',
                                     'Ethernet1/18',
                                     'Ethernet1/19',
                                     'Ethernet1/20',
                                     'Ethernet1/21',
                                     'Ethernet1/22',
                                     'Ethernet1/23',
                                     'Ethernet1/24',
                                     'Ethernet1/25',
                                     'Ethernet1/26',
                                     'Ethernet1/27',
                                     'Ethernet1/28',
                                     'Ethernet1/29',
                                     'Ethernet1/30',
                                     'Ethernet1/31',
                                     'Ethernet1/32',
                                     'Ethernet1/33',
                                     'Ethernet1/34',
                                     'Ethernet1/35',
                                     'Ethernet1/36',
                                     'Ethernet1/37',
                                     'Ethernet1/38',
                                     'Ethernet1/39',
                                     'Ethernet1/40',
                                     'Ethernet1/41',
                                     'Ethernet1/42',
                                     'Ethernet1/43',
                                     'Ethernet1/44',
                                     'Ethernet1/45',
                                     'Ethernet1/46',
                                     'Ethernet1/47',
                                     'Ethernet1/48',
                                     'Ethernet1/49',
                                     'Ethernet1/50',
                                     'Ethernet1/51',
                                     'Ethernet1/52',
                                     'Ethernet1/53',
                                     'Ethernet1/54',
                                     'Ethernet1/55',
                                     'Ethernet1/56',
                                     'Ethernet1/57',
                                     'Ethernet1/58',
                                     'Ethernet1/59',
                                     'Ethernet1/60',
                                     'Ethernet1/61',
                                     'Ethernet1/62',
                                     'Ethernet1/63',
                                     'Ethernet1/64',
                                     'port-channel11',
                                     'loopback1',
                                     'loopback30',
                                     'loopback98',
                                     'loopback99',
                                     'Vlan1',
                                     'Vlan100',
                                     'Vlan101',
                                     'Vlan102',
                                     'Vlan103',
                                     'Vlan104',
                                     'Vlan105'],
                 'model': 'Nexus9000 C9300v Chassis',
                 'os_version': '',
                 'serial_number': '9QXOX90PJ62',
                 'uptime': 15870,
                 'vendor': 'Cisco'}}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Decomposing Nornir Result Object of type <class 'nornir.core.task.AggregatedResult'>...

Iterating through result object of type<class 'nornir.core.task.MultiResult'> for item ios-xe-mgmt
        Get the top level key(s) for the device:
        dict_keys(['get_facts'])

        Get the next level of key(s):
        dict_keys(['uptime', 'vendor', 'os_version', 'serial_number', 'model', 'hostname', 'fqdn', 'interface_list'])
        Decomposing Result Object for hostname ios-xe-mgmt...
                Key uptime       has Value: 49560
                Key vendor       has Value: Cisco
                Key os_version   has Value: Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.9.3, RELEASE SOFTWARE (fc2)
                Key serial_number        has Value: 9XXJEG7SFU4
                Key model        has Value: CSR1000V
                Key hostname     has Value: csr1000v
                Key fqdn         has Value: csr1000v.abc.inc
                Key interface_list       has Value: ['GigabitEthernet1', 'GigabitEthernet2', 'GigabitEthernet3', 'Loopback2', 'Loopback10', 'Loopback103', 'Loopback120', 'Loopback200', 'VirtualPortGroup0']


Iterating through result object of type<class 'nornir.core.task.MultiResult'> for item sbx-nxos-mgmt
        Get the top level key(s) for the device:
        dict_keys(['get_facts'])

        Get the next level of key(s):
        dict_keys(['vendor', 'serial_number', 'model', 'hostname', 'os_version', 'uptime', 'interface_list', 'fqdn'])
        Decomposing Result Object for hostname sbx-nxos-mgmt...
                Key vendor       has Value: Cisco
                Key serial_number        has Value: 9QXOX90PJ62
                Key model        has Value: Nexus9000 C9300v Chassis
                Key hostname     has Value: sbx-n9kv-ao
                Key os_version   has Value: 
                Key uptime       has Value: 15870
                Key interface_list       has Value: ['mgmt0', 'Ethernet1/1', 'Ethernet1/2', 'Ethernet1/3', 'Ethernet1/4', 'Ethernet1/5', 'Ethernet1/6', 'Ethernet1/7', 'Ethernet1/8', 'Ethernet1/9', 'Ethernet1/10', 'Ethernet1/11', 'Ethernet1/12', 'Ethernet1/13', 'Ethernet1/14', 'Ethernet1/15', 'Ethernet1/16', 'Ethernet1/17', 'Ethernet1/18', 'Ethernet1/19', 'Ethernet1/20', 'Ethernet1/21', 'Ethernet1/22', 'Ethernet1/23', 'Ethernet1/24', 'Ethernet1/25', 'Ethernet1/26', 'Ethernet1/27', 'Ethernet1/28', 'Ethernet1/29', 'Ethernet1/30', 'Ethernet1/31', 'Ethernet1/32', 'Ethernet1/33', 'Ethernet1/34', 'Ethernet1/35', 'Ethernet1/36', 'Ethernet1/37', 'Ethernet1/38', 'Ethernet1/39', 'Ethernet1/40', 'Ethernet1/41', 'Ethernet1/42', 'Ethernet1/43', 'Ethernet1/44', 'Ethernet1/45', 'Ethernet1/46', 'Ethernet1/47', 'Ethernet1/48', 'Ethernet1/49', 'Ethernet1/50', 'Ethernet1/51', 'Ethernet1/52', 'Ethernet1/53', 'Ethernet1/54', 'Ethernet1/55', 'Ethernet1/56', 'Ethernet1/57', 'Ethernet1/58', 'Ethernet1/59', 'Ethernet1/60', 'Ethernet1/61', 'Ethernet1/62', 'Ethernet1/63', 'Ethernet1/64', 'port-channel11', 'loopback1', 'loopback30', 'loopback98', 'loopback99', 'Vlan1', 'Vlan100', 'Vlan101', 'Vlan102', 'Vlan103', 'Vlan104', 'Vlan105']
                Key fqdn         has Value: sbx-n9kv-ao



Print run results with the print_result module.
This is a built-in Ansible like run status that will format the output for easy viewing...
napalm_get**********************************************************************
* ios-xe-mgmt ** changed : False ***********************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'get_facts': { 'fqdn': 'csr1000v.abc.inc',
                 'hostname': 'csr1000v',
                 'interface_list': [ 'GigabitEthernet1',
                                     'GigabitEthernet2',
                                     'GigabitEthernet3',
                                     'Loopback2',
                                     'Loopback10',
                                     'Loopback103',
                                     'Loopback120',
                                     'Loopback200',
                                     'VirtualPortGroup0'],
                 'model': 'CSR1000V',
                 'os_version': 'Virtual XE Software '
                               '(X86_64_LINUX_IOSD-UNIVERSALK9-M), Version '
                               '16.9.3, RELEASE SOFTWARE (fc2)',
                 'serial_number': '9XXJEG7SFU4',
                 'uptime': 49560,
                 'vendor': 'Cisco'}}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* sbx-nxos-mgmt ** changed : False *********************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'get_facts': { 'fqdn': 'sbx-n9kv-ao',
                 'hostname': 'sbx-n9kv-ao',
                 'interface_list': [ 'mgmt0',
                                     'Ethernet1/1',
                                     'Ethernet1/2',
                                     'Ethernet1/3',
                                     'Ethernet1/4',
                                     'Ethernet1/5',
                                     'Ethernet1/6',
                                     'Ethernet1/7',
                                     'Ethernet1/8',
                                     'Ethernet1/9',
                                     'Ethernet1/10',
                                     'Ethernet1/11',
                                     'Ethernet1/12',
                                     'Ethernet1/13',
                                     'Ethernet1/14',
                                     'Ethernet1/15',
                                     'Ethernet1/16',
                                     'Ethernet1/17',
                                     'Ethernet1/18',
                                     'Ethernet1/19',
                                     'Ethernet1/20',
                                     'Ethernet1/21',
                                     'Ethernet1/22',
                                     'Ethernet1/23',
                                     'Ethernet1/24',
                                     'Ethernet1/25',
                                     'Ethernet1/26',
                                     'Ethernet1/27',
                                     'Ethernet1/28',
                                     'Ethernet1/29',
                                     'Ethernet1/30',
                                     'Ethernet1/31',
                                     'Ethernet1/32',
                                     'Ethernet1/33',
                                     'Ethernet1/34',
                                     'Ethernet1/35',
                                     'Ethernet1/36',
                                     'Ethernet1/37',
                                     'Ethernet1/38',
                                     'Ethernet1/39',
                                     'Ethernet1/40',
                                     'Ethernet1/41',
                                     'Ethernet1/42',
                                     'Ethernet1/43',
                                     'Ethernet1/44',
                                     'Ethernet1/45',
                                     'Ethernet1/46',
                                     'Ethernet1/47',
                                     'Ethernet1/48',
                                     'Ethernet1/49',
                                     'Ethernet1/50',
                                     'Ethernet1/51',
                                     'Ethernet1/52',
                                     'Ethernet1/53',
                                     'Ethernet1/54',
                                     'Ethernet1/55',
                                     'Ethernet1/56',
                                     'Ethernet1/57',
                                     'Ethernet1/58',
                                     'Ethernet1/59',
                                     'Ethernet1/60',
                                     'Ethernet1/61',
                                     'Ethernet1/62',
                                     'Ethernet1/63',
                                     'Ethernet1/64',
                                     'port-channel11',
                                     'loopback1',
                                     'loopback30',
                                     'loopback98',
                                     'loopback99',
                                     'Vlan1',
                                     'Vlan100',
                                     'Vlan101',
                                     'Vlan102',
                                     'Vlan103',
                                     'Vlan104',
                                     'Vlan105'],
                 'model': 'Nexus9000 C9300v Chassis',
                 'os_version': '',
                 'serial_number': '9QXOX90PJ62',
                 'uptime': 15870,
                 'vendor': 'Cisco'}}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(nornir) claudia@Claudias-iMac nornir_intro2 % 



```



For more examples you can review:

[Configuration Creation with Nornir](https://gratuitous-arp.net/configuration-creation-with-nornir/)



## Licensing

This code is licensed under the BSD 3-Clause License. See [LICENSE](https://github.com/CiscoDevNet/code-exchange-repo-template/blob/master/manual-sample-repo/LICENSE) for details.

