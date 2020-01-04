# Example from Patrick Ogenstad at Networklore
# https://networklore.com/introducing-brigade/
from brigade.core import InitBrigade
from brigade.plugins.tasks.networking import napalm_get
from brigade.plugins.functions.text import print_result

brg = InitBrigade()

result = brg.run(
             napalm_get,
             getters=['get_facts'])

print_result(result)