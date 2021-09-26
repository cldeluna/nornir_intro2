# Example from Patrick Ogenstad at Networklore
# Updated for nornir3
# https://networklore.com/introducing-brigade/
from nornir import InitNornir
# Updated to plugin modules
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get


nr = InitNornir()

result = nr.run(
             napalm_get,
             getters=['get_facts'])

print_result(result)
