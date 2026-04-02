# compiled_pyke_files.py

from pyke import target_pkg

pyke_version = '1.1.1'
compiler_version = 1
target_pkg_version = 1

try:
    loader = __loader__
except NameError:
    loader = None

def get_target_pkg():
    return target_pkg.target_pkg(__name__, __file__, pyke_version, loader, {
         ('animal_expert_system.knowledge_es2', '', 'animals.kfb'):
           [1775162097.3739295, 'animals.fbc'],
         ('animal_expert_system.knowledge_es2', '', 'animal_rules_bc.krb'):
           [1775162097.3790872, 'animal_rules_bc_bc.py'],
         ('animal_expert_system.knowledge_es2', '', 'animal_rules_fc.krb'):
           [1775162097.3868732, 'animal_rules_fc_fc.py'],
        },
        compiler_version)

