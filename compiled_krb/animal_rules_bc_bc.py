# animal_rules_bc_bc.py

from pyke import contexts, pattern, bc_rule

pyke_version = '1.1.1'
compiler_version = 1

def taxonomy_accipitriformes(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove(rule.rule_base.root_name, 'diurnal_accipiter_raptor', context,
                          (rule.pattern(0),
                           rule.pattern(1),
                           rule.pattern(2),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "animal_rules_bc.taxonomy_accipitriformes: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def taxonomy_strigiformes(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove(rule.rule_base.root_name, 'nocturnal_strigiforme_raptor', context,
                          (rule.pattern(0),
                           rule.pattern(1),
                           rule.pattern(2),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "animal_rules_bc.taxonomy_strigiformes: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def taxonomy_passeriformes(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove(rule.rule_base.root_name, 'perching_passeriforme', context,
                          (rule.pattern(0),
                           rule.pattern(1),
                           rule.pattern(2),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "animal_rules_bc.taxonomy_passeriformes: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def taxonomy_psittaciformes(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove(rule.rule_base.root_name, 'parrot_psittaciforme', context,
                          (rule.pattern(0),
                           rule.pattern(1),
                           rule.pattern(2),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "animal_rules_bc.taxonomy_psittaciformes: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def taxonomy_columbiformes(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove(rule.rule_base.root_name, 'pigeon_columbiforme', context,
                          (rule.pattern(0),
                           rule.pattern(1),
                           rule.pattern(2),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "animal_rules_bc.taxonomy_columbiformes: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def taxonomy_charadriiformes(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove(rule.rule_base.root_name, 'gull_charadriforme', context,
                          (rule.pattern(0),
                           rule.pattern(1),
                           rule.pattern(2),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "animal_rules_bc.taxonomy_charadriiformes: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def taxonomy_pelecaniformes(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove(rule.rule_base.root_name, 'pelecan_pelecaniforme', context,
                          (rule.pattern(0),
                           rule.pattern(1),
                           rule.pattern(2),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "animal_rules_bc.taxonomy_pelecaniformes: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def taxonomy_gruiformes(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove(rule.rule_base.root_name, 'crane_gruiforme', context,
                          (rule.pattern(0),
                           rule.pattern(1),
                           rule.pattern(2),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "animal_rules_bc.taxonomy_gruiformes: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def diurnal_accipiter_raptor(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('animals', 'bird_profile', context,
                          (rule.pattern(0),
                           rule.pattern(1),
                           rule.pattern(1),
                           rule.pattern(2),
                           rule.pattern(3),
                           rule.pattern(4),
                           rule.pattern(5),
                           rule.pattern(6),
                           rule.pattern(7),
                           rule.pattern(8),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "animal_rules_bc.diurnal_accipiter_raptor: got unexpected plan from when clause 1"
            with engine.prove('animals', 'characteristic', context,
                              (rule.pattern(9),
                               rule.pattern(4),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "animal_rules_bc.diurnal_accipiter_raptor: got unexpected plan from when clause 2"
                with engine.prove('animals', 'characteristic', context,
                                  (rule.pattern(10),
                                   rule.pattern(5),)) \
                  as gen_3:
                  for x_3 in gen_3:
                    assert x_3 is None, \
                      "animal_rules_bc.diurnal_accipiter_raptor: got unexpected plan from when clause 3"
                    with engine.prove('animals', 'characteristic', context,
                                      (rule.pattern(11),
                                       rule.pattern(6),)) \
                      as gen_4:
                      for x_4 in gen_4:
                        assert x_4 is None, \
                          "animal_rules_bc.diurnal_accipiter_raptor: got unexpected plan from when clause 4"
                        with engine.prove('animals', 'characteristic', context,
                                          (rule.pattern(12),
                                           rule.pattern(7),)) \
                          as gen_5:
                          for x_5 in gen_5:
                            assert x_5 is None, \
                              "animal_rules_bc.diurnal_accipiter_raptor: got unexpected plan from when clause 5"
                            with engine.prove('animals', 'characteristic', context,
                                              (rule.pattern(13),
                                               rule.pattern(8),)) \
                              as gen_6:
                              for x_6 in gen_6:
                                assert x_6 is None, \
                                  "animal_rules_bc.diurnal_accipiter_raptor: got unexpected plan from when clause 6"
                                rule.rule_base.num_bc_rule_successes += 1
                                yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def nocturnal_strigiforme_raptor(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('animals', 'bird_profile', context,
                          (rule.pattern(0),
                           rule.pattern(1),
                           rule.pattern(1),
                           rule.pattern(2),
                           rule.pattern(3),
                           rule.pattern(4),
                           rule.pattern(5),
                           rule.pattern(6),
                           rule.pattern(7),
                           rule.pattern(8),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "animal_rules_bc.nocturnal_strigiforme_raptor: got unexpected plan from when clause 1"
            with engine.prove('animals', 'characteristic', context,
                              (rule.pattern(9),
                               rule.pattern(4),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "animal_rules_bc.nocturnal_strigiforme_raptor: got unexpected plan from when clause 2"
                with engine.prove('animals', 'characteristic', context,
                                  (rule.pattern(10),
                                   rule.pattern(5),)) \
                  as gen_3:
                  for x_3 in gen_3:
                    assert x_3 is None, \
                      "animal_rules_bc.nocturnal_strigiforme_raptor: got unexpected plan from when clause 3"
                    with engine.prove('animals', 'characteristic', context,
                                      (rule.pattern(11),
                                       rule.pattern(6),)) \
                      as gen_4:
                      for x_4 in gen_4:
                        assert x_4 is None, \
                          "animal_rules_bc.nocturnal_strigiforme_raptor: got unexpected plan from when clause 4"
                        with engine.prove('animals', 'characteristic', context,
                                          (rule.pattern(12),
                                           rule.pattern(7),)) \
                          as gen_5:
                          for x_5 in gen_5:
                            assert x_5 is None, \
                              "animal_rules_bc.nocturnal_strigiforme_raptor: got unexpected plan from when clause 5"
                            with engine.prove('animals', 'characteristic', context,
                                              (rule.pattern(13),
                                               rule.pattern(8),)) \
                              as gen_6:
                              for x_6 in gen_6:
                                assert x_6 is None, \
                                  "animal_rules_bc.nocturnal_strigiforme_raptor: got unexpected plan from when clause 6"
                                rule.rule_base.num_bc_rule_successes += 1
                                yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def perching_passeriforme(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('animals', 'bird_profile', context,
                          (rule.pattern(0),
                           rule.pattern(1),
                           rule.pattern(1),
                           rule.pattern(2),
                           rule.pattern(3),
                           rule.pattern(4),
                           rule.pattern(5),
                           rule.pattern(6),
                           rule.pattern(7),
                           rule.pattern(8),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "animal_rules_bc.perching_passeriforme: got unexpected plan from when clause 1"
            with engine.prove('animals', 'characteristic', context,
                              (rule.pattern(9),
                               rule.pattern(4),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "animal_rules_bc.perching_passeriforme: got unexpected plan from when clause 2"
                with engine.prove('animals', 'characteristic', context,
                                  (rule.pattern(10),
                                   rule.pattern(5),)) \
                  as gen_3:
                  for x_3 in gen_3:
                    assert x_3 is None, \
                      "animal_rules_bc.perching_passeriforme: got unexpected plan from when clause 3"
                    with engine.prove('animals', 'characteristic', context,
                                      (rule.pattern(11),
                                       rule.pattern(6),)) \
                      as gen_4:
                      for x_4 in gen_4:
                        assert x_4 is None, \
                          "animal_rules_bc.perching_passeriforme: got unexpected plan from when clause 4"
                        with engine.prove('animals', 'characteristic', context,
                                          (rule.pattern(12),
                                           rule.pattern(7),)) \
                          as gen_5:
                          for x_5 in gen_5:
                            assert x_5 is None, \
                              "animal_rules_bc.perching_passeriforme: got unexpected plan from when clause 5"
                            with engine.prove('animals', 'characteristic', context,
                                              (rule.pattern(13),
                                               rule.pattern(8),)) \
                              as gen_6:
                              for x_6 in gen_6:
                                assert x_6 is None, \
                                  "animal_rules_bc.perching_passeriforme: got unexpected plan from when clause 6"
                                rule.rule_base.num_bc_rule_successes += 1
                                yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def parrot_psittaciforme(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('animals', 'bird_profile', context,
                          (rule.pattern(0),
                           rule.pattern(1),
                           rule.pattern(1),
                           rule.pattern(2),
                           rule.pattern(3),
                           rule.pattern(4),
                           rule.pattern(5),
                           rule.pattern(6),
                           rule.pattern(7),
                           rule.pattern(8),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "animal_rules_bc.parrot_psittaciforme: got unexpected plan from when clause 1"
            with engine.prove('animals', 'characteristic', context,
                              (rule.pattern(9),
                               rule.pattern(4),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "animal_rules_bc.parrot_psittaciforme: got unexpected plan from when clause 2"
                with engine.prove('animals', 'characteristic', context,
                                  (rule.pattern(10),
                                   rule.pattern(5),)) \
                  as gen_3:
                  for x_3 in gen_3:
                    assert x_3 is None, \
                      "animal_rules_bc.parrot_psittaciforme: got unexpected plan from when clause 3"
                    with engine.prove('animals', 'characteristic', context,
                                      (rule.pattern(11),
                                       rule.pattern(6),)) \
                      as gen_4:
                      for x_4 in gen_4:
                        assert x_4 is None, \
                          "animal_rules_bc.parrot_psittaciforme: got unexpected plan from when clause 4"
                        with engine.prove('animals', 'characteristic', context,
                                          (rule.pattern(12),
                                           rule.pattern(7),)) \
                          as gen_5:
                          for x_5 in gen_5:
                            assert x_5 is None, \
                              "animal_rules_bc.parrot_psittaciforme: got unexpected plan from when clause 5"
                            with engine.prove('animals', 'characteristic', context,
                                              (rule.pattern(13),
                                               rule.pattern(8),)) \
                              as gen_6:
                              for x_6 in gen_6:
                                assert x_6 is None, \
                                  "animal_rules_bc.parrot_psittaciforme: got unexpected plan from when clause 6"
                                rule.rule_base.num_bc_rule_successes += 1
                                yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def pigeon_columbiforme(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('animals', 'bird_profile', context,
                          (rule.pattern(0),
                           rule.pattern(1),
                           rule.pattern(1),
                           rule.pattern(2),
                           rule.pattern(3),
                           rule.pattern(4),
                           rule.pattern(5),
                           rule.pattern(6),
                           rule.pattern(7),
                           rule.pattern(8),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "animal_rules_bc.pigeon_columbiforme: got unexpected plan from when clause 1"
            with engine.prove('animals', 'characteristic', context,
                              (rule.pattern(9),
                               rule.pattern(4),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "animal_rules_bc.pigeon_columbiforme: got unexpected plan from when clause 2"
                with engine.prove('animals', 'characteristic', context,
                                  (rule.pattern(10),
                                   rule.pattern(5),)) \
                  as gen_3:
                  for x_3 in gen_3:
                    assert x_3 is None, \
                      "animal_rules_bc.pigeon_columbiforme: got unexpected plan from when clause 3"
                    with engine.prove('animals', 'characteristic', context,
                                      (rule.pattern(11),
                                       rule.pattern(6),)) \
                      as gen_4:
                      for x_4 in gen_4:
                        assert x_4 is None, \
                          "animal_rules_bc.pigeon_columbiforme: got unexpected plan from when clause 4"
                        with engine.prove('animals', 'characteristic', context,
                                          (rule.pattern(12),
                                           rule.pattern(7),)) \
                          as gen_5:
                          for x_5 in gen_5:
                            assert x_5 is None, \
                              "animal_rules_bc.pigeon_columbiforme: got unexpected plan from when clause 5"
                            with engine.prove('animals', 'characteristic', context,
                                              (rule.pattern(13),
                                               rule.pattern(8),)) \
                              as gen_6:
                              for x_6 in gen_6:
                                assert x_6 is None, \
                                  "animal_rules_bc.pigeon_columbiforme: got unexpected plan from when clause 6"
                                rule.rule_base.num_bc_rule_successes += 1
                                yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def gull_charadriforme(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('animals', 'bird_profile', context,
                          (rule.pattern(0),
                           rule.pattern(1),
                           rule.pattern(1),
                           rule.pattern(2),
                           rule.pattern(3),
                           rule.pattern(4),
                           rule.pattern(5),
                           rule.pattern(6),
                           rule.pattern(7),
                           rule.pattern(8),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "animal_rules_bc.gull_charadriforme: got unexpected plan from when clause 1"
            with engine.prove('animals', 'characteristic', context,
                              (rule.pattern(9),
                               rule.pattern(4),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "animal_rules_bc.gull_charadriforme: got unexpected plan from when clause 2"
                with engine.prove('animals', 'characteristic', context,
                                  (rule.pattern(10),
                                   rule.pattern(5),)) \
                  as gen_3:
                  for x_3 in gen_3:
                    assert x_3 is None, \
                      "animal_rules_bc.gull_charadriforme: got unexpected plan from when clause 3"
                    with engine.prove('animals', 'characteristic', context,
                                      (rule.pattern(11),
                                       rule.pattern(6),)) \
                      as gen_4:
                      for x_4 in gen_4:
                        assert x_4 is None, \
                          "animal_rules_bc.gull_charadriforme: got unexpected plan from when clause 4"
                        with engine.prove('animals', 'characteristic', context,
                                          (rule.pattern(12),
                                           rule.pattern(7),)) \
                          as gen_5:
                          for x_5 in gen_5:
                            assert x_5 is None, \
                              "animal_rules_bc.gull_charadriforme: got unexpected plan from when clause 5"
                            with engine.prove('animals', 'characteristic', context,
                                              (rule.pattern(13),
                                               rule.pattern(8),)) \
                              as gen_6:
                              for x_6 in gen_6:
                                assert x_6 is None, \
                                  "animal_rules_bc.gull_charadriforme: got unexpected plan from when clause 6"
                                rule.rule_base.num_bc_rule_successes += 1
                                yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def pelecan_pelecaniforme(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('animals', 'bird_profile', context,
                          (rule.pattern(0),
                           rule.pattern(1),
                           rule.pattern(1),
                           rule.pattern(2),
                           rule.pattern(3),
                           rule.pattern(4),
                           rule.pattern(5),
                           rule.pattern(6),
                           rule.pattern(7),
                           rule.pattern(8),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "animal_rules_bc.pelecan_pelecaniforme: got unexpected plan from when clause 1"
            with engine.prove('animals', 'characteristic', context,
                              (rule.pattern(9),
                               rule.pattern(4),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "animal_rules_bc.pelecan_pelecaniforme: got unexpected plan from when clause 2"
                with engine.prove('animals', 'characteristic', context,
                                  (rule.pattern(10),
                                   rule.pattern(5),)) \
                  as gen_3:
                  for x_3 in gen_3:
                    assert x_3 is None, \
                      "animal_rules_bc.pelecan_pelecaniforme: got unexpected plan from when clause 3"
                    with engine.prove('animals', 'characteristic', context,
                                      (rule.pattern(11),
                                       rule.pattern(6),)) \
                      as gen_4:
                      for x_4 in gen_4:
                        assert x_4 is None, \
                          "animal_rules_bc.pelecan_pelecaniforme: got unexpected plan from when clause 4"
                        with engine.prove('animals', 'characteristic', context,
                                          (rule.pattern(12),
                                           rule.pattern(7),)) \
                          as gen_5:
                          for x_5 in gen_5:
                            assert x_5 is None, \
                              "animal_rules_bc.pelecan_pelecaniforme: got unexpected plan from when clause 5"
                            with engine.prove('animals', 'characteristic', context,
                                              (rule.pattern(13),
                                               rule.pattern(8),)) \
                              as gen_6:
                              for x_6 in gen_6:
                                assert x_6 is None, \
                                  "animal_rules_bc.pelecan_pelecaniforme: got unexpected plan from when clause 6"
                                rule.rule_base.num_bc_rule_successes += 1
                                yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def crane_gruiforme(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('animals', 'bird_profile', context,
                          (rule.pattern(0),
                           rule.pattern(1),
                           rule.pattern(1),
                           rule.pattern(2),
                           rule.pattern(3),
                           rule.pattern(4),
                           rule.pattern(5),
                           rule.pattern(6),
                           rule.pattern(7),
                           rule.pattern(8),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "animal_rules_bc.crane_gruiforme: got unexpected plan from when clause 1"
            with engine.prove('animals', 'characteristic', context,
                              (rule.pattern(9),
                               rule.pattern(4),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "animal_rules_bc.crane_gruiforme: got unexpected plan from when clause 2"
                with engine.prove('animals', 'characteristic', context,
                                  (rule.pattern(10),
                                   rule.pattern(5),)) \
                  as gen_3:
                  for x_3 in gen_3:
                    assert x_3 is None, \
                      "animal_rules_bc.crane_gruiforme: got unexpected plan from when clause 3"
                    with engine.prove('animals', 'characteristic', context,
                                      (rule.pattern(11),
                                       rule.pattern(6),)) \
                      as gen_4:
                      for x_4 in gen_4:
                        assert x_4 is None, \
                          "animal_rules_bc.crane_gruiforme: got unexpected plan from when clause 4"
                        with engine.prove('animals', 'characteristic', context,
                                          (rule.pattern(12),
                                           rule.pattern(7),)) \
                          as gen_5:
                          for x_5 in gen_5:
                            assert x_5 is None, \
                              "animal_rules_bc.crane_gruiforme: got unexpected plan from when clause 5"
                            with engine.prove('animals', 'characteristic', context,
                                              (rule.pattern(13),
                                               rule.pattern(8),)) \
                              as gen_6:
                              for x_6 in gen_6:
                                assert x_6 is None, \
                                  "animal_rules_bc.crane_gruiforme: got unexpected plan from when clause 6"
                                rule.rule_base.num_bc_rule_successes += 1
                                yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def populate(engine):
  This_rule_base = engine.get_create('animal_rules_bc')
  
  bc_rule.bc_rule('taxonomy_accipitriformes', This_rule_base, 'taxonomy',
                  taxonomy_accipitriformes, None,
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),),
                  (),
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),))
  
  bc_rule.bc_rule('taxonomy_strigiformes', This_rule_base, 'taxonomy',
                  taxonomy_strigiformes, None,
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),),
                  (),
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),))
  
  bc_rule.bc_rule('taxonomy_passeriformes', This_rule_base, 'taxonomy',
                  taxonomy_passeriformes, None,
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),),
                  (),
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),))
  
  bc_rule.bc_rule('taxonomy_psittaciformes', This_rule_base, 'taxonomy',
                  taxonomy_psittaciformes, None,
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),),
                  (),
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),))
  
  bc_rule.bc_rule('taxonomy_columbiformes', This_rule_base, 'taxonomy',
                  taxonomy_columbiformes, None,
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),),
                  (),
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),))
  
  bc_rule.bc_rule('taxonomy_charadriiformes', This_rule_base, 'taxonomy',
                  taxonomy_charadriiformes, None,
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),),
                  (),
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),))
  
  bc_rule.bc_rule('taxonomy_pelecaniformes', This_rule_base, 'taxonomy',
                  taxonomy_pelecaniformes, None,
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),),
                  (),
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),))
  
  bc_rule.bc_rule('taxonomy_gruiformes', This_rule_base, 'taxonomy',
                  taxonomy_gruiformes, None,
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),),
                  (),
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),))
  
  bc_rule.bc_rule('diurnal_accipiter_raptor', This_rule_base, 'diurnal_accipiter_raptor',
                  diurnal_accipiter_raptor, None,
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),),
                  (),
                  (contexts.variable('bird_id'),
                   contexts.anonymous('_'),
                   contexts.variable('order'),
                   contexts.variable('family'),
                   contexts.variable('habitat'),
                   contexts.variable('diet'),
                   contexts.variable('morphology'),
                   contexts.variable('size'),
                   contexts.variable('activity'),
                   pattern.pattern_literal('habitat'),
                   pattern.pattern_literal('diet'),
                   pattern.pattern_literal('morphology'),
                   pattern.pattern_literal('size'),
                   pattern.pattern_literal('activity'),))
  
  bc_rule.bc_rule('nocturnal_strigiforme_raptor', This_rule_base, 'nocturnal_strigiforme_raptor',
                  nocturnal_strigiforme_raptor, None,
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),),
                  (),
                  (contexts.variable('bird_id'),
                   contexts.anonymous('_'),
                   contexts.variable('order'),
                   contexts.variable('family'),
                   contexts.variable('habitat'),
                   contexts.variable('diet'),
                   contexts.variable('morphology'),
                   contexts.variable('size'),
                   contexts.variable('activity'),
                   pattern.pattern_literal('habitat'),
                   pattern.pattern_literal('diet'),
                   pattern.pattern_literal('morphology'),
                   pattern.pattern_literal('size'),
                   pattern.pattern_literal('activity'),))
  
  bc_rule.bc_rule('perching_passeriforme', This_rule_base, 'perching_passeriforme',
                  perching_passeriforme, None,
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),),
                  (),
                  (contexts.variable('bird_id'),
                   contexts.anonymous('_'),
                   contexts.variable('order'),
                   contexts.variable('family'),
                   contexts.variable('habitat'),
                   contexts.variable('diet'),
                   contexts.variable('morphology'),
                   contexts.variable('size'),
                   contexts.variable('activity'),
                   pattern.pattern_literal('habitat'),
                   pattern.pattern_literal('diet'),
                   pattern.pattern_literal('morphology'),
                   pattern.pattern_literal('size'),
                   pattern.pattern_literal('activity'),))
  
  bc_rule.bc_rule('parrot_psittaciforme', This_rule_base, 'parrot_psittaciforme',
                  parrot_psittaciforme, None,
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),),
                  (),
                  (contexts.variable('bird_id'),
                   contexts.anonymous('_'),
                   contexts.variable('order'),
                   contexts.variable('family'),
                   contexts.variable('habitat'),
                   contexts.variable('diet'),
                   contexts.variable('morphology'),
                   contexts.variable('size'),
                   contexts.variable('activity'),
                   pattern.pattern_literal('habitat'),
                   pattern.pattern_literal('diet'),
                   pattern.pattern_literal('morphology'),
                   pattern.pattern_literal('size'),
                   pattern.pattern_literal('activity'),))
  
  bc_rule.bc_rule('pigeon_columbiforme', This_rule_base, 'pigeon_columbiforme',
                  pigeon_columbiforme, None,
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),),
                  (),
                  (contexts.variable('bird_id'),
                   contexts.anonymous('_'),
                   contexts.variable('order'),
                   contexts.variable('family'),
                   contexts.variable('habitat'),
                   contexts.variable('diet'),
                   contexts.variable('morphology'),
                   contexts.variable('size'),
                   contexts.variable('activity'),
                   pattern.pattern_literal('habitat'),
                   pattern.pattern_literal('diet'),
                   pattern.pattern_literal('morphology'),
                   pattern.pattern_literal('size'),
                   pattern.pattern_literal('activity'),))
  
  bc_rule.bc_rule('gull_charadriforme', This_rule_base, 'gull_charadriforme',
                  gull_charadriforme, None,
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),),
                  (),
                  (contexts.variable('bird_id'),
                   contexts.anonymous('_'),
                   contexts.variable('order'),
                   contexts.variable('family'),
                   contexts.variable('habitat'),
                   contexts.variable('diet'),
                   contexts.variable('morphology'),
                   contexts.variable('size'),
                   contexts.variable('activity'),
                   pattern.pattern_literal('habitat'),
                   pattern.pattern_literal('diet'),
                   pattern.pattern_literal('morphology'),
                   pattern.pattern_literal('size'),
                   pattern.pattern_literal('activity'),))
  
  bc_rule.bc_rule('pelecan_pelecaniforme', This_rule_base, 'pelecan_pelecaniforme',
                  pelecan_pelecaniforme, None,
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),),
                  (),
                  (contexts.variable('bird_id'),
                   contexts.anonymous('_'),
                   contexts.variable('order'),
                   contexts.variable('family'),
                   contexts.variable('habitat'),
                   contexts.variable('diet'),
                   contexts.variable('morphology'),
                   contexts.variable('size'),
                   contexts.variable('activity'),
                   pattern.pattern_literal('habitat'),
                   pattern.pattern_literal('diet'),
                   pattern.pattern_literal('morphology'),
                   pattern.pattern_literal('size'),
                   pattern.pattern_literal('activity'),))
  
  bc_rule.bc_rule('crane_gruiforme', This_rule_base, 'crane_gruiforme',
                  crane_gruiforme, None,
                  (contexts.variable('bird_id'),
                   contexts.variable('order'),
                   contexts.variable('family'),),
                  (),
                  (contexts.variable('bird_id'),
                   contexts.anonymous('_'),
                   contexts.variable('order'),
                   contexts.variable('family'),
                   contexts.variable('habitat'),
                   contexts.variable('diet'),
                   contexts.variable('morphology'),
                   contexts.variable('size'),
                   contexts.variable('activity'),
                   pattern.pattern_literal('habitat'),
                   pattern.pattern_literal('diet'),
                   pattern.pattern_literal('morphology'),
                   pattern.pattern_literal('size'),
                   pattern.pattern_literal('activity'),))


Krb_filename = '..\\src\\animal_expert_system\\knowledge\\animal_rules_bc.krb'
Krb_lineno_map = (
    ((14, 18), (5, 5)),
    ((20, 27), (7, 7)),
    ((40, 44), (10, 10)),
    ((46, 53), (12, 12)),
    ((66, 70), (15, 15)),
    ((72, 79), (17, 17)),
    ((92, 96), (20, 20)),
    ((98, 105), (22, 22)),
    ((118, 122), (25, 25)),
    ((124, 131), (27, 27)),
    ((144, 148), (30, 30)),
    ((150, 157), (32, 32)),
    ((170, 174), (35, 35)),
    ((176, 183), (37, 37)),
    ((196, 200), (40, 40)),
    ((202, 209), (42, 42)),
    ((222, 226), (46, 46)),
    ((228, 242), (48, 49)),
    ((243, 249), (50, 50)),
    ((250, 256), (51, 51)),
    ((257, 263), (52, 52)),
    ((264, 270), (53, 53)),
    ((271, 277), (54, 54)),
    ((290, 294), (58, 58)),
    ((296, 310), (60, 61)),
    ((311, 317), (62, 62)),
    ((318, 324), (63, 63)),
    ((325, 331), (64, 64)),
    ((332, 338), (65, 65)),
    ((339, 345), (66, 66)),
    ((358, 362), (70, 70)),
    ((364, 378), (72, 73)),
    ((379, 385), (74, 74)),
    ((386, 392), (75, 75)),
    ((393, 399), (76, 76)),
    ((400, 406), (77, 77)),
    ((407, 413), (78, 78)),
    ((426, 430), (82, 82)),
    ((432, 446), (84, 85)),
    ((447, 453), (86, 86)),
    ((454, 460), (87, 87)),
    ((461, 467), (88, 88)),
    ((468, 474), (89, 89)),
    ((475, 481), (90, 90)),
    ((494, 498), (94, 94)),
    ((500, 514), (96, 97)),
    ((515, 521), (98, 98)),
    ((522, 528), (99, 99)),
    ((529, 535), (100, 100)),
    ((536, 542), (101, 101)),
    ((543, 549), (102, 102)),
    ((562, 566), (106, 106)),
    ((568, 582), (108, 109)),
    ((583, 589), (110, 110)),
    ((590, 596), (111, 111)),
    ((597, 603), (112, 112)),
    ((604, 610), (113, 113)),
    ((611, 617), (114, 114)),
    ((630, 634), (118, 118)),
    ((636, 650), (120, 121)),
    ((651, 657), (122, 122)),
    ((658, 664), (123, 123)),
    ((665, 671), (124, 124)),
    ((672, 678), (125, 125)),
    ((679, 685), (126, 126)),
    ((698, 702), (130, 130)),
    ((704, 718), (132, 133)),
    ((719, 725), (134, 134)),
    ((726, 732), (135, 135)),
    ((733, 739), (136, 136)),
    ((740, 746), (137, 137)),
    ((747, 753), (138, 138)),
)
