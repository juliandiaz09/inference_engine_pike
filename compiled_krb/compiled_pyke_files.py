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
         ('', 'src\\animal_expert_system\\knowledge', 'animals.kfb'):
           [1775448474.9048016, 'animals.fbc'],
         ('', 'src\\animal_expert_system\\knowledge', 'animal_rules.krb'):
           [1775448474.9158063, 'animal_rules_fc.py'],
         ('', 'src\\animal_expert_system\\knowledge', 'animal_rules_bc.krb'):
           [1775448474.9554307, 'animal_rules_bc_bc.py'],
         ('', 'src\\animal_expert_system\\knowledge', 'animal_rules_fc.krb'):
           [1775448474.9758868, 'animal_rules_fc_fc.py'],
        },
        compiler_version)

