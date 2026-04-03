# animal_rules_bc_bc.py

from pyke import contexts, pattern, bc_rule

pyke_version = '1.1.1'
compiler_version = 1

def taxonomia(rule, arg_patterns, arg_context):
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
        with engine.prove('animales', 'perfil_animal', context,
                          (rule.pattern(0),
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
              "animal_rules_bc.taxonomia: got unexpected plan from when clause 1"
            with engine.prove('animales', 'caracteristica', context,
                              (rule.pattern(9),
                               rule.pattern(4),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "animal_rules_bc.taxonomia: got unexpected plan from when clause 2"
                with engine.prove('animales', 'caracteristica', context,
                                  (rule.pattern(10),
                                   rule.pattern(5),)) \
                  as gen_3:
                  for x_3 in gen_3:
                    assert x_3 is None, \
                      "animal_rules_bc.taxonomia: got unexpected plan from when clause 3"
                    with engine.prove('animales', 'caracteristica', context,
                                      (rule.pattern(11),
                                       rule.pattern(6),)) \
                      as gen_4:
                      for x_4 in gen_4:
                        assert x_4 is None, \
                          "animal_rules_bc.taxonomia: got unexpected plan from when clause 4"
                        with engine.prove('animales', 'caracteristica', context,
                                          (rule.pattern(12),
                                           rule.pattern(7),)) \
                          as gen_5:
                          for x_5 in gen_5:
                            assert x_5 is None, \
                              "animal_rules_bc.taxonomia: got unexpected plan from when clause 5"
                            with engine.prove('animales', 'caracteristica', context,
                                              (rule.pattern(13),
                                               rule.pattern(8),)) \
                              as gen_6:
                              for x_6 in gen_6:
                                assert x_6 is None, \
                                  "animal_rules_bc.taxonomia: got unexpected plan from when clause 6"
                                rule.rule_base.num_bc_rule_successes += 1
                                yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def populate(engine):
  This_rule_base = engine.get_create('animal_rules_bc')
  
  bc_rule.bc_rule('taxonomia', This_rule_base, 'taxonomia',
                  taxonomia, None,
                  (contexts.variable('animal'),
                   contexts.variable('clase'),
                   contexts.variable('orden'),
                   contexts.variable('familia'),),
                  (),
                  (contexts.variable('animal'),
                   contexts.variable('clase'),
                   contexts.variable('orden'),
                   contexts.variable('familia'),
                   contexts.variable('habitat'),
                   contexts.variable('dieta'),
                   contexts.variable('morfologia'),
                   contexts.variable('reproduccion'),
                   contexts.variable('actividad'),
                   pattern.pattern_literal('habitat'),
                   pattern.pattern_literal('diet'),
                   pattern.pattern_literal('morphology'),
                   pattern.pattern_literal('reproduction'),
                   pattern.pattern_literal('activity'),))


Krb_filename = '..\\animal_rules_bc.krb'
Krb_lineno_map = (
    ((14, 18), (4, 4)),
    ((20, 33), (6, 8)),
    ((34, 40), (9, 9)),
    ((41, 47), (10, 10)),
    ((48, 54), (11, 11)),
    ((55, 61), (12, 12)),
    ((62, 68), (13, 13)),
)
