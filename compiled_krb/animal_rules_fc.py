# animal_rules_fc.py

from pyke import contexts, pattern, fc_rule, knowledge_base

pyke_version = '1.1.1'
compiler_version = 1

def profile_match(rule, context = None, index = None):
  engine = rule.rule_base.engine
  if context is None: context = contexts.simple_context()
  try:
    with knowledge_base.Gen_once if index == 0 \
             else engine.lookup('animals', 'bird_profile', context,
                                rule.foreach_patterns(0)) \
      as gen_0:
      for dummy in gen_0:
        with knowledge_base.Gen_once if index == 1 \
                 else engine.lookup('animals', 'characteristic', context,
                                    rule.foreach_patterns(1)) \
          as gen_1:
          for dummy in gen_1:
            with knowledge_base.Gen_once if index == 2 \
                     else engine.lookup('animals', 'characteristic', context,
                                        rule.foreach_patterns(2)) \
              as gen_2:
              for dummy in gen_2:
                with knowledge_base.Gen_once if index == 3 \
                         else engine.lookup('animals', 'characteristic', context,
                                            rule.foreach_patterns(3)) \
                  as gen_3:
                  for dummy in gen_3:
                    with knowledge_base.Gen_once if index == 4 \
                             else engine.lookup('animals', 'characteristic', context,
                                                rule.foreach_patterns(4)) \
                      as gen_4:
                      for dummy in gen_4:
                        with knowledge_base.Gen_once if index == 5 \
                                 else engine.lookup('animals', 'characteristic', context,
                                                    rule.foreach_patterns(5)) \
                          as gen_5:
                          for dummy in gen_5:
                            engine.assert_('animals', 'candidate',
                                           (rule.pattern(0).as_data(context),)),
                            engine.assert_('animals', 'taxonomy',
                                           (rule.pattern(0).as_data(context),
                                            rule.pattern(1).as_data(context),
                                            rule.pattern(2).as_data(context),)),
                            rule.rule_base.num_fc_rules_triggered += 1
  finally:
    context.done()

def taxonomy_from_candidate(rule, context = None, index = None):
  engine = rule.rule_base.engine
  if context is None: context = contexts.simple_context()
  try:
    with knowledge_base.Gen_once if index == 0 \
             else engine.lookup('animals', 'candidate', context,
                                rule.foreach_patterns(0)) \
      as gen_0:
      for dummy in gen_0:
        with knowledge_base.Gen_once if index == 1 \
                 else engine.lookup('animals', 'bird_profile', context,
                                    rule.foreach_patterns(1)) \
          as gen_1:
          for dummy in gen_1:
            engine.assert_('animals', 'classification',
                           (rule.pattern(0).as_data(context),
                            rule.pattern(1).as_data(context),)),
            engine.assert_('animals', 'classification',
                           (rule.pattern(2).as_data(context),
                            rule.pattern(3).as_data(context),)),
            engine.assert_('animals', 'classification',
                           (rule.pattern(4).as_data(context),
                            rule.pattern(5).as_data(context),)),
            rule.rule_base.num_fc_rules_triggered += 1
  finally:
    context.done()

def populate(engine):
  This_rule_base = engine.get_create('animal_rules')
  
  fc_rule.fc_rule('profile_match', This_rule_base, profile_match,
    (('animals', 'bird_profile',
      (contexts.variable('bird_id'),
       contexts.variable('scientific_name'),
       contexts.variable('class_name'),
       contexts.variable('order'),
       contexts.variable('family'),
       contexts.variable('habitat'),
       contexts.variable('diet'),
       contexts.variable('morphology'),
       contexts.variable('size'),
       contexts.variable('activity'),),
      False),
     ('animals', 'characteristic',
      (pattern.pattern_literal('habitat'),
       contexts.variable('habitat'),),
      False),
     ('animals', 'characteristic',
      (pattern.pattern_literal('diet'),
       contexts.variable('diet'),),
      False),
     ('animals', 'characteristic',
      (pattern.pattern_literal('morphology'),
       contexts.variable('morphology'),),
      False),
     ('animals', 'characteristic',
      (pattern.pattern_literal('size'),
       contexts.variable('size'),),
      False),
     ('animals', 'characteristic',
      (pattern.pattern_literal('activity'),
       contexts.variable('activity'),),
      False),),
    (contexts.variable('bird_id'),
     contexts.variable('order'),
     contexts.variable('family'),))
  
  fc_rule.fc_rule('taxonomy_from_candidate', This_rule_base, taxonomy_from_candidate,
    (('animals', 'candidate',
      (contexts.variable('bird_id'),),
      False),
     ('animals', 'bird_profile',
      (contexts.variable('bird_id'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       contexts.variable('order'),
       contexts.variable('family'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),),
      False),),
    (pattern.pattern_literal('class'),
     pattern.pattern_literal('Aves'),
     pattern.pattern_literal('order'),
     contexts.variable('order'),
     pattern.pattern_literal('family'),
     contexts.variable('family'),))


Krb_filename = '..\\src\\animal_expert_system\\knowledge\\animal_rules.krb'
Krb_lineno_map = (
    ((12, 16), (5, 6)),
    ((17, 21), (7, 7)),
    ((22, 26), (8, 8)),
    ((27, 31), (9, 9)),
    ((32, 36), (10, 10)),
    ((37, 41), (11, 11)),
    ((42, 43), (13, 13)),
    ((44, 47), (14, 14)),
    ((56, 60), (19, 19)),
    ((61, 65), (20, 20)),
    ((66, 68), (22, 22)),
    ((69, 71), (23, 23)),
    ((72, 74), (24, 24)),
)
