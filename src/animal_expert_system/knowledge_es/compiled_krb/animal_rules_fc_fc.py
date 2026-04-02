# animal_rules_fc_fc.py

from pyke import contexts, pattern, fc_rule, knowledge_base

pyke_version = '1.1.1'
compiler_version = 1

def perfil_coincidente(rule, context = None, index = None):
  engine = rule.rule_base.engine
  if context is None: context = contexts.simple_context()
  try:
    with knowledge_base.Gen_once if index == 0 \
             else engine.lookup('animales', 'perfil_animal', context,
                                rule.foreach_patterns(0)) \
      as gen_0:
      for dummy in gen_0:
        with knowledge_base.Gen_once if index == 1 \
                 else engine.lookup('animales', 'caracteristica', context,
                                    rule.foreach_patterns(1)) \
          as gen_1:
          for dummy in gen_1:
            with knowledge_base.Gen_once if index == 2 \
                     else engine.lookup('animales', 'caracteristica', context,
                                        rule.foreach_patterns(2)) \
              as gen_2:
              for dummy in gen_2:
                with knowledge_base.Gen_once if index == 3 \
                         else engine.lookup('animales', 'caracteristica', context,
                                            rule.foreach_patterns(3)) \
                  as gen_3:
                  for dummy in gen_3:
                    with knowledge_base.Gen_once if index == 4 \
                             else engine.lookup('animales', 'caracteristica', context,
                                                rule.foreach_patterns(4)) \
                      as gen_4:
                      for dummy in gen_4:
                        with knowledge_base.Gen_once if index == 5 \
                                 else engine.lookup('animales', 'caracteristica', context,
                                                    rule.foreach_patterns(5)) \
                          as gen_5:
                          for dummy in gen_5:
                            engine.assert_('animales', 'candidato',
                                           (rule.pattern(0).as_data(context),)),
                            engine.assert_('animales', 'taxonomia',
                                           (rule.pattern(0).as_data(context),
                                            rule.pattern(1).as_data(context),
                                            rule.pattern(2).as_data(context),
                                            rule.pattern(3).as_data(context),)),
                            rule.rule_base.num_fc_rules_triggered += 1
  finally:
    context.done()

def populate(engine):
  This_rule_base = engine.get_create('animal_rules_fc')
  
  fc_rule.fc_rule('perfil_coincidente', This_rule_base, perfil_coincidente,
    (('animales', 'perfil_animal',
      (contexts.variable('animal'),
       contexts.variable('clase'),
       contexts.variable('orden'),
       contexts.variable('familia'),
       contexts.variable('habitat'),
       contexts.variable('dieta'),
       contexts.variable('morfologia'),
       contexts.variable('reproduccion'),
       contexts.variable('actividad'),),
      False),
     ('animales', 'caracteristica',
      (pattern.pattern_literal('habitat'),
       contexts.variable('habitat'),),
      False),
     ('animales', 'caracteristica',
      (pattern.pattern_literal('diet'),
       contexts.variable('dieta'),),
      False),
     ('animales', 'caracteristica',
      (pattern.pattern_literal('morphology'),
       contexts.variable('morfologia'),),
      False),
     ('animales', 'caracteristica',
      (pattern.pattern_literal('reproduction'),
       contexts.variable('reproduccion'),),
      False),
     ('animales', 'caracteristica',
      (pattern.pattern_literal('activity'),
       contexts.variable('actividad'),),
      False),),
    (contexts.variable('animal'),
     contexts.variable('clase'),
     contexts.variable('orden'),
     contexts.variable('familia'),))


Krb_filename = '..\\animal_rules_fc.krb'
Krb_lineno_map = (
    ((12, 16), (5, 7)),
    ((17, 21), (8, 8)),
    ((22, 26), (9, 9)),
    ((27, 31), (10, 10)),
    ((32, 36), (11, 11)),
    ((37, 41), (12, 12)),
    ((42, 43), (14, 14)),
    ((44, 48), (15, 15)),
)
