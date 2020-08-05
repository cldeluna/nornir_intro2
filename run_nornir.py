git # Example from Patrick Ogenstad at Networklore
# Updated for nornir
# https://networklore.com/introducing-brigade/
from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result


nr = InitNornir()

result = nr.run(
             napalm_get,
             getters=['get_facts'])

print_result(result)
