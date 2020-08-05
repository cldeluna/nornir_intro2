# First Nornir (formerly brigade) Test Run
## Get Facts

## Summary

This repository accompanies my post [Nornir – A New Network Automation Framework](https://gratuitous-arp.net/nornir-a-new-network-automation-framework/) and is my first test of the network automation framework formerly known as brigade (and now known as Nornir - not responsible for alliteration!).

This was my first use of Nornir so the code has lots of comments as I figured stuff out.  I started out with the sample get facts *run\_nornir.py* script from from [Patrick Ogenstad at Networklore.](https://networklore.com/introducing-brigade/)

I'm fairly excited about this!  It took me about 45 minutes to get things set up on my Windows 10 system.  It took almost no time at all on my Mac.

Using PyCharm on my mac the **print_result** output is formatted and color coded nicely.  Using PyCharm on my Windows 10 system the output is less colorful.

The ***first\_nornir.py*** script is my attempt to take the basics from Mr. Ogenstad's example script and decompose the objects and resulting data structures.  It took me a while the first time and with Nornir2 it took me even longer!  It makes complete sense and these objects are highly flexible but for someone newish to Python it nearly made my head explode.  Luckily, with cranium still intact, I'm still very excited about this framework!   

Having said that, if you are not comfortable with some of these more complex data structures please see [Decomposing Data Structures](https://gratuitous-arp.net/decomposing-complex-json-data-structures/) or sign up for one of [Kirk Byers](https://pynet.twb-tech.com/) Python for Network Engineers courses!

My next Sunday afternoon project will involve [generating configurations and applying them](https://gratuitous-arp.net/configuration-creation-with-nornir/).

## Code Example

Like Ansible, Nornir will leverage inventory information.  Here you see a very basic **groups.yaml** file which
can also contain a default section for more general values and a **hosts.yaml** file which can reference specific or more general group settings defined in the groups.yaml file.  These files can take any **key:value** pair and the values with the "nornir_" prefix have special meaning as you would expect.



### Files that set up your environment and devices

Note: The scripts in the repository comment out local devices and retain DevNet Always On devices so that the scripts can be run immediately with results.  Local devices are left if for example purposes only.  The output shown below uses local devices.

###### groups.yaml

```
  ---
  uwaco_network:
    platform: ios
    username: cisco
    password: cisco
  devnet_sandbox_iosxe:
    platform: ios
    username: root
    password: D_Vay!_10&
    port: 8181   
```

###### hosts.yaml

        ---
        eu-med-as01:
          hostname: 10.1.10.25
          groups: ['uwaco_network']
    
        arctic-ds01-as01:
          hostname: 10.1.10.26
          groups: ['uwaco_network']
        
        ios-xe-mgmt:
          hostname: ios-xe-mgmt.cisco.com
          groups: ['devnet_sandbox_iosxe']   



#### Scripts in the Repository

| Script            |                                                              |
| ----------------- | ------------------------------------------------------------ |
| run\_nornir.py    | Sample nornir script using napalm get facts from from Patrick Ogenstad at Networklore |
| first\_nornir.py  | Building on Patrick Ogenstad run_nornir.py script, this script works through understanding the returned objects and structured data. |
| netmiko_nornir.py | Now that we are little familiar with the basics of Nornir, let's use Nornir with Netmiko to get the output of specific commands rather than the structured data returned by Napalm facts. |


The first part of the **first_nornir.py** script initializes a nornir object called **nr**.  This reads in the host information and the script shows how to get to some of that information.

Next, we use the run method on the nr object..well..to run some commands which in this case uses napalm to get facts.

The next sections of the script attempt to deconstruct the objects into workable values like getting the keys of all the hosts.

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

Print run results with the print_result module.
This is a built-in Ansible like run status that will format the output for easy viewing...
napalm_get**********************************************************************
* arctic-ds01-as01 ** changed : False ******************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'get_facts': { 'fqdn': 'mgmt-sw05.uwaco.net',
                 'hostname': 'mgmt-sw05',
                 'interface_list': [ 'Vlan1',
                                     'Vlan30',
                                     'Vlan100',
                                     'Vlan101',
                                     'FastEthernet1/0/1',
                                     'FastEthernet1/0/2',
                                     'FastEthernet1/0/3',
                                     'FastEthernet1/0/4',
                                     'FastEthernet1/0/5',
                                     'FastEthernet1/0/6',
                                     'FastEthernet1/0/7',
                                     'FastEthernet1/0/8',
                                     'FastEthernet1/0/9',
                                     'FastEthernet1/0/10',
                                     'FastEthernet1/0/11',
                                     'FastEthernet1/0/12',
                                     'FastEthernet1/0/13',
                                     'FastEthernet1/0/14',
                                     'FastEthernet1/0/15',
                                     'FastEthernet1/0/16',
                                     'FastEthernet1/0/17',
                                     'FastEthernet1/0/18',
                                     'FastEthernet1/0/19',
                                     'FastEthernet1/0/20',
                                     'FastEthernet1/0/21',
                                     'FastEthernet1/0/22',
                                     'FastEthernet1/0/23',
                                     'FastEthernet1/0/24',
                                     'FastEthernet1/0/25',
                                     'FastEthernet1/0/26',
                                     'FastEthernet1/0/27',
                                     'FastEthernet1/0/28',
                                     'FastEthernet1/0/29',
                                     'FastEthernet1/0/30',
                                     'FastEthernet1/0/31',
                                     'FastEthernet1/0/32',
                                     'FastEthernet1/0/33',
                                     'FastEthernet1/0/34',
                                     'FastEthernet1/0/35',
                                     'FastEthernet1/0/36',
                                     'FastEthernet1/0/37',
                                     'FastEthernet1/0/38',
                                     'FastEthernet1/0/39',
                                     'FastEthernet1/0/40',
                                     'FastEthernet1/0/41',
                                     'FastEthernet1/0/42',
                                     'FastEthernet1/0/43',
                                     'FastEthernet1/0/44',
                                     'FastEthernet1/0/45',
                                     'FastEthernet1/0/46',
                                     'FastEthernet1/0/47',
                                     'FastEthernet1/0/48',
                                     'GigabitEthernet1/0/1',
                                     'GigabitEthernet1/0/2',
                                     'GigabitEthernet1/0/3',
                                     'GigabitEthernet1/0/4',
                                     'FastEthernet2/0/1',
                                     'FastEthernet2/0/2',
                                     'FastEthernet2/0/3',
                                     'FastEthernet2/0/4',
                                     'FastEthernet2/0/5',
                                     'FastEthernet2/0/6',
                                     'FastEthernet2/0/7',
                                     'FastEthernet2/0/8',
                                     'FastEthernet2/0/9',
                                     'FastEthernet2/0/10',
                                     'FastEthernet2/0/11',
                                     'FastEthernet2/0/12',
                                     'FastEthernet2/0/13',
                                     'FastEthernet2/0/14',
                                     'FastEthernet2/0/15',
                                     'FastEthernet2/0/16',
                                     'FastEthernet2/0/17',
                                     'FastEthernet2/0/18',
                                     'FastEthernet2/0/19',
                                     'FastEthernet2/0/20',
                                     'FastEthernet2/0/21',
                                     'FastEthernet2/0/22',
                                     'FastEthernet2/0/23',
                                     'FastEthernet2/0/24',
                                     'FastEthernet2/0/25',
                                     'FastEthernet2/0/26',
                                     'FastEthernet2/0/27',
                                     'FastEthernet2/0/28',
                                     'FastEthernet2/0/29',
                                     'FastEthernet2/0/30',
                                     'FastEthernet2/0/31',
                                     'FastEthernet2/0/32',
                                     'FastEthernet2/0/33',
                                     'FastEthernet2/0/34',
                                     'FastEthernet2/0/35',
                                     'FastEthernet2/0/36',
                                     'FastEthernet2/0/37',
                                     'FastEthernet2/0/38',
                                     'FastEthernet2/0/39',
                                     'FastEthernet2/0/40',
                                     'FastEthernet2/0/41',
                                     'FastEthernet2/0/42',
                                     'FastEthernet2/0/43',
                                     'FastEthernet2/0/44',
                                     'FastEthernet2/0/45',
                                     'FastEthernet2/0/46',
                                     'FastEthernet2/0/47',
                                     'FastEthernet2/0/48',
                                     'GigabitEthernet2/0/1',
                                     'GigabitEthernet2/0/2',
                                     'GigabitEthernet2/0/3',
                                     'GigabitEthernet2/0/4'],
                 'model': 'WS-C3750-48TS',
                 'os_version': 'C3750 Software (C3750-IPSERVICESK9-M), Version '
                               '12.2(55)SE3, RELEASE SOFTWARE (fc1)',
                 'serial_number': 'CAT1012345T',
                 'uptime': 9360,
                 'vendor': 'Cisco'}}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* eu-med-as01 ** changed : False ***********************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'get_facts': { 'fqdn': 'eu-med-as01.uwaco.net',
                 'hostname': 'eu-med-as01',
                 'interface_list': [ 'Vlan1',
                                     'Vlan10',
                                     'Vlan11',
                                     'Vlan12',
                                     'Vlan100',
                                     'Vlan101',
                                     'Vlan102',
                                     'Vlan103',
                                     'Vlan104',
                                     'Vlan105',
                                     'Vlan106',
                                     'Vlan107',
                                     'Vlan108',
                                     'Vlan109',
                                     'Vlan110',
                                     'Vlan111',
                                     'Vlan112',
                                     'Vlan114',
                                     'Vlan115',
                                     'Vlan116',
                                     'Vlan117',
                                     'Vlan118',
                                     'Vlan120',
                                     'Vlan122',
                                     'Vlan123',
                                     'Vlan124',
                                     'Vlan125',
                                     'Vlan126',
                                     'Vlan128',
                                     'Vlan131',
                                     'Vlan136',
                                     'Vlan137',
                                     'Vlan138',
                                     'Vlan139',
                                     'Vlan140',
                                     'Vlan188',
                                     'Vlan200',
                                     'Vlan201',
                                     'Vlan202',
                                     'Vlan203',
                                     'Vlan204',
                                     'Vlan205',
                                     'Vlan206',
                                     'Vlan207',
                                     'Vlan208',
                                     'Vlan209',
                                     'Vlan210',
                                     'Vlan211',
                                     'Vlan212',
                                     'Vlan213',
                                     'Vlan214',
                                     'Vlan215',
                                     'Vlan216',
                                     'Vlan217',
                                     'Vlan218',
                                     'Vlan220',
                                     'Vlan222',
                                     'Vlan223',
                                     'Vlan228',
                                     'Vlan236',
                                     'Vlan240',
                                     'Vlan600',
                                     'Vlan601',
                                     'Vlan602',
                                     'Vlan700',
                                     'Vlan701',
                                     'Vlan800',
                                     'GigabitEthernet0/0',
                                     'GigabitEthernet1/0/1',
                                     'GigabitEthernet1/0/2',
                                     'GigabitEthernet1/0/3',
                                     'GigabitEthernet1/0/4',
                                     'GigabitEthernet1/0/5',
                                     'GigabitEthernet1/0/6',
                                     'GigabitEthernet1/0/7',
                                     'GigabitEthernet1/0/8',
                                     'GigabitEthernet1/0/9',
                                     'GigabitEthernet1/0/10',
                                     'GigabitEthernet1/0/11',
                                     'GigabitEthernet1/0/12',
                                     'GigabitEthernet1/0/13',
                                     'GigabitEthernet1/0/14',
                                     'GigabitEthernet1/0/15',
                                     'GigabitEthernet1/0/16',
                                     'GigabitEthernet1/0/17',
                                     'GigabitEthernet1/0/18',
                                     'GigabitEthernet1/0/19',
                                     'GigabitEthernet1/0/20',
                                     'GigabitEthernet1/0/21',
                                     'GigabitEthernet1/0/22',
                                     'GigabitEthernet1/0/23',
                                     'GigabitEthernet1/0/24',
                                     'GigabitEthernet1/1/1',
                                     'GigabitEthernet1/1/2',
                                     'GigabitEthernet1/1/3',
                                     'GigabitEthernet1/1/4',
                                     'Te1/1/1',
                                     'Te1/1/2',
                                     'Te1/1/3',
                                     'Te1/1/4',
                                     'GigabitEthernet2/0/1',
                                     'GigabitEthernet2/0/2',
                                     'GigabitEthernet2/0/3',
                                     'GigabitEthernet2/0/4',
                                     'GigabitEthernet2/0/5',
                                     'GigabitEthernet2/0/6',
                                     'GigabitEthernet2/0/7',
                                     'GigabitEthernet2/0/8',
                                     'GigabitEthernet2/0/9',
                                     'GigabitEthernet2/0/10',
                                     'GigabitEthernet2/0/11',
                                     'GigabitEthernet2/0/12',
                                     'GigabitEthernet2/0/13',
                                     'GigabitEthernet2/0/14',
                                     'GigabitEthernet2/0/15',
                                     'GigabitEthernet2/0/16',
                                     'GigabitEthernet2/0/17',
                                     'GigabitEthernet2/0/18',
                                     'GigabitEthernet2/0/19',
                                     'GigabitEthernet2/0/20',
                                     'GigabitEthernet2/0/21',
                                     'GigabitEthernet2/0/22',
                                     'GigabitEthernet2/0/23',
                                     'GigabitEthernet2/0/24',
                                     'GigabitEthernet2/1/1',
                                     'GigabitEthernet2/1/2',
                                     'GigabitEthernet2/1/3',
                                     'GigabitEthernet2/1/4',
                                     'Te2/1/1',
                                     'Te2/1/2',
                                     'Te2/1/3',
                                     'Te2/1/4',
                                     'GigabitEthernet3/0/1',
                                     'GigabitEthernet3/0/2',
                                     'GigabitEthernet3/0/3',
                                     'GigabitEthernet3/0/4',
                                     'GigabitEthernet3/0/5',
                                     'GigabitEthernet3/0/6',
                                     'GigabitEthernet3/0/7',
                                     'GigabitEthernet3/0/8',
                                     'GigabitEthernet3/0/9',
                                     'GigabitEthernet3/0/10',
                                     'GigabitEthernet3/0/11',
                                     'GigabitEthernet3/0/12',
                                     'GigabitEthernet3/0/13',
                                     'GigabitEthernet3/0/14',
                                     'GigabitEthernet3/0/15',
                                     'GigabitEthernet3/0/16',
                                     'GigabitEthernet3/0/17',
                                     'GigabitEthernet3/0/18',
                                     'GigabitEthernet3/0/19',
                                     'GigabitEthernet3/0/20',
                                     'GigabitEthernet3/0/21',
                                     'GigabitEthernet3/0/22',
                                     'GigabitEthernet3/0/23',
                                     'GigabitEthernet3/0/24',
                                     'GigabitEthernet3/1/1',
                                     'GigabitEthernet3/1/2',
                                     'GigabitEthernet3/1/3',
                                     'GigabitEthernet3/1/4',
                                     'Te3/1/1',
                                     'Te3/1/2',
                                     'Te3/1/3',
                                     'Te3/1/4',
                                     'GigabitEthernet4/0/1',
                                     'GigabitEthernet4/0/2',
                                     'GigabitEthernet4/0/3',
                                     'GigabitEthernet4/0/4',
                                     'GigabitEthernet4/0/5',
                                     'GigabitEthernet4/0/6',
                                     'GigabitEthernet4/0/7',
                                     'GigabitEthernet4/0/8',
                                     'GigabitEthernet4/0/9',
                                     'GigabitEthernet4/0/10',
                                     'GigabitEthernet4/0/11',
                                     'GigabitEthernet4/0/12',
                                     'GigabitEthernet4/0/13',
                                     'GigabitEthernet4/0/14',
                                     'GigabitEthernet4/0/15',
                                     'GigabitEthernet4/0/16',
                                     'GigabitEthernet4/0/17',
                                     'GigabitEthernet4/0/18',
                                     'GigabitEthernet4/0/19',
                                     'GigabitEthernet4/0/20',
                                     'GigabitEthernet4/0/21',
                                     'GigabitEthernet4/0/22',
                                     'GigabitEthernet4/0/23',
                                     'GigabitEthernet4/0/24',
                                     'GigabitEthernet4/1/1',
                                     'GigabitEthernet4/1/2',
                                     'GigabitEthernet4/1/3',
                                     'GigabitEthernet4/1/4',
                                     'Te4/1/1',
                                     'Te4/1/2',
                                     'Te4/1/3',
                                     'Te4/1/4',
                                     'GigabitEthernet5/0/1',
                                     'GigabitEthernet5/0/2',
                                     'GigabitEthernet5/0/3',
                                     'GigabitEthernet5/0/4',
                                     'GigabitEthernet5/0/5',
                                     'GigabitEthernet5/0/6',
                                     'GigabitEthernet5/0/7',
                                     'GigabitEthernet5/0/8',
                                     'GigabitEthernet5/0/9',
                                     'GigabitEthernet5/0/10',
                                     'GigabitEthernet5/0/11',
                                     'GigabitEthernet5/0/12',
                                     'GigabitEthernet5/0/13',
                                     'GigabitEthernet5/0/14',
                                     'GigabitEthernet5/0/15',
                                     'GigabitEthernet5/0/16',
                                     'GigabitEthernet5/0/17',
                                     'GigabitEthernet5/0/18',
                                     'GigabitEthernet5/0/19',
                                     'GigabitEthernet5/0/20',
                                     'GigabitEthernet5/0/21',
                                     'GigabitEthernet5/0/22',
                                     'GigabitEthernet5/0/23',
                                     'GigabitEthernet5/0/24',
                                     'GigabitEthernet5/1/1',
                                     'GigabitEthernet5/1/2',
                                     'GigabitEthernet5/1/3',
                                     'GigabitEthernet5/1/4',
                                     'Te5/1/1',
                                     'Te5/1/2',
                                     'Te5/1/3',
                                     'Te5/1/4',
                                     'GigabitEthernet6/0/1',
                                     'GigabitEthernet6/0/2',
                                     'GigabitEthernet6/0/3',
                                     'GigabitEthernet6/0/4',
                                     'GigabitEthernet6/0/5',
                                     'GigabitEthernet6/0/6',
                                     'GigabitEthernet6/0/7',
                                     'GigabitEthernet6/0/8',
                                     'GigabitEthernet6/0/9',
                                     'GigabitEthernet6/0/10',
                                     'GigabitEthernet6/0/11',
                                     'GigabitEthernet6/0/12',
                                     'GigabitEthernet6/0/13',
                                     'GigabitEthernet6/0/14',
                                     'GigabitEthernet6/0/15',
                                     'GigabitEthernet6/0/16',
                                     'GigabitEthernet6/0/17',
                                     'GigabitEthernet6/0/18',
                                     'GigabitEthernet6/0/19',
                                     'GigabitEthernet6/0/20',
                                     'GigabitEthernet6/0/21',
                                     'GigabitEthernet6/0/22',
                                     'GigabitEthernet6/0/23',
                                     'GigabitEthernet6/0/24',
                                     'GigabitEthernet6/1/1',
                                     'GigabitEthernet6/1/2',
                                     'GigabitEthernet6/1/3',
                                     'GigabitEthernet6/1/4',
                                     'Te6/1/1',
                                     'Te6/1/2',
                                     'Te6/1/3',
                                     'Te6/1/4'],
                 'model': 'WS-C3850-24P',
                 'os_version': 'Catalyst L3 Switch Software '
                               '(CAT3K_CAA-UNIVERSALK9-M), Version 16.6.2, '
                               'RELEASE SOFTWARE (fc2)',
                 'serial_number': 'FOC876Fg45L',
                 'uptime': 21120,
                 'vendor': 'Cisco'}}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


```



