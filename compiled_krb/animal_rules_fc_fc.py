# animal_rules_fc_fc.py

from pyke import contexts, pattern, fc_rule, knowledge_base

pyke_version = '1.1.1'
compiler_version = 1

def identify_diurnal_raptor_species(rule, context = None, index = None):
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

def classify_accipiter_diurnal(rule, context = None, index = None):
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
            rule.rule_base.num_fc_rules_triggered += 1
  finally:
    context.done()

def classify_strigiforme_nocturnal(rule, context = None, index = None):
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
            rule.rule_base.num_fc_rules_triggered += 1
  finally:
    context.done()

def classify_passeriforme(rule, context = None, index = None):
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
            rule.rule_base.num_fc_rules_triggered += 1
  finally:
    context.done()

def classify_psittaciforme_parrot(rule, context = None, index = None):
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
            rule.rule_base.num_fc_rules_triggered += 1
  finally:
    context.done()

def classify_columbiforme_pigeon(rule, context = None, index = None):
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
            rule.rule_base.num_fc_rules_triggered += 1
  finally:
    context.done()

def classify_charadriforme_gull(rule, context = None, index = None):
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
            rule.rule_base.num_fc_rules_triggered += 1
  finally:
    context.done()

def classify_pelecaniforme(rule, context = None, index = None):
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
            rule.rule_base.num_fc_rules_triggered += 1
  finally:
    context.done()

def classify_gruiforme_crane(rule, context = None, index = None):
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
            rule.rule_base.num_fc_rules_triggered += 1
  finally:
    context.done()

def populate(engine):
  This_rule_base = engine.get_create('animal_rules_fc')
  
  fc_rule.fc_rule('identify_diurnal_raptor_species', This_rule_base, identify_diurnal_raptor_species,
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
  
  fc_rule.fc_rule('classify_accipiter_diurnal', This_rule_base, classify_accipiter_diurnal,
    (('animals', 'candidate',
      (contexts.variable('bird_id'),),
      False),
     ('animals', 'bird_profile',
      (contexts.variable('bird_id'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       pattern.pattern_literal('Accipitriformes'),
       pattern.pattern_literal('Accipitridae'),
       contexts.anonymous('_'),
       pattern.pattern_literal('carnivore'),
       pattern.pattern_literal('hooked_beak'),
       contexts.anonymous('_'),
       pattern.pattern_literal('diurnal'),),
      False),),
    (pattern.pattern_literal('order'),
     pattern.pattern_literal('Accipitriformes'),
     pattern.pattern_literal('family'),
     pattern.pattern_literal('Accipitridae'),))
  
  fc_rule.fc_rule('classify_strigiforme_nocturnal', This_rule_base, classify_strigiforme_nocturnal,
    (('animals', 'candidate',
      (contexts.variable('bird_id'),),
      False),
     ('animals', 'bird_profile',
      (contexts.variable('bird_id'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       pattern.pattern_literal('Strigiformes'),
       contexts.variable('family'),
       contexts.anonymous('_'),
       pattern.pattern_literal('carnivore'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       pattern.pattern_literal('nocturnal'),),
      False),),
    (pattern.pattern_literal('order'),
     pattern.pattern_literal('Strigiformes'),
     pattern.pattern_literal('family'),
     contexts.variable('family'),))
  
  fc_rule.fc_rule('classify_passeriforme', This_rule_base, classify_passeriforme,
    (('animals', 'candidate',
      (contexts.variable('bird_id'),),
      False),
     ('animals', 'bird_profile',
      (contexts.variable('bird_id'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       pattern.pattern_literal('Passeriformes'),
       contexts.variable('family'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       pattern.pattern_literal('diurnal'),),
      False),),
    (pattern.pattern_literal('order'),
     pattern.pattern_literal('Passeriformes'),
     pattern.pattern_literal('family'),
     contexts.variable('family'),))
  
  fc_rule.fc_rule('classify_psittaciforme_parrot', This_rule_base, classify_psittaciforme_parrot,
    (('animals', 'candidate',
      (contexts.variable('bird_id'),),
      False),
     ('animals', 'bird_profile',
      (contexts.variable('bird_id'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       pattern.pattern_literal('Psittaciformes'),
       pattern.pattern_literal('Psittacidae'),
       pattern.pattern_literal('rainforest'),
       pattern.pattern_literal('herbivore'),
       pattern.pattern_literal('curved_beak'),
       pattern.pattern_literal('large'),
       pattern.pattern_literal('diurnal'),),
      False),),
    (pattern.pattern_literal('order'),
     pattern.pattern_literal('Psittaciformes'),
     pattern.pattern_literal('family'),
     pattern.pattern_literal('Psittacidae'),))
  
  fc_rule.fc_rule('classify_columbiforme_pigeon', This_rule_base, classify_columbiforme_pigeon,
    (('animals', 'candidate',
      (contexts.variable('bird_id'),),
      False),
     ('animals', 'bird_profile',
      (contexts.variable('bird_id'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       pattern.pattern_literal('Columbiformes'),
       pattern.pattern_literal('Columbidae'),
       pattern.pattern_literal('urban'),
       pattern.pattern_literal('herbivore'),
       pattern.pattern_literal('straight_beak'),
       pattern.pattern_literal('medium'),
       pattern.pattern_literal('diurnal'),),
      False),),
    (pattern.pattern_literal('order'),
     pattern.pattern_literal('Columbiformes'),
     pattern.pattern_literal('family'),
     pattern.pattern_literal('Columbidae'),))
  
  fc_rule.fc_rule('classify_charadriforme_gull', This_rule_base, classify_charadriforme_gull,
    (('animals', 'candidate',
      (contexts.variable('bird_id'),),
      False),
     ('animals', 'bird_profile',
      (contexts.variable('bird_id'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       pattern.pattern_literal('Charadriiformes'),
       pattern.pattern_literal('Laridae'),
       pattern.pattern_literal('coastal'),
       pattern.pattern_literal('omnivore'),
       pattern.pattern_literal('webbed_feet'),
       pattern.pattern_literal('medium'),
       pattern.pattern_literal('diurnal'),),
      False),),
    (pattern.pattern_literal('order'),
     pattern.pattern_literal('Charadriiformes'),
     pattern.pattern_literal('family'),
     pattern.pattern_literal('Laridae'),))
  
  fc_rule.fc_rule('classify_pelecaniforme', This_rule_base, classify_pelecaniforme,
    (('animals', 'candidate',
      (contexts.variable('bird_id'),),
      False),
     ('animals', 'bird_profile',
      (contexts.variable('bird_id'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       pattern.pattern_literal('Pelecaniformes'),
       contexts.variable('family'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       pattern.pattern_literal('diurnal'),),
      False),),
    (pattern.pattern_literal('order'),
     pattern.pattern_literal('Pelecaniformes'),
     pattern.pattern_literal('family'),
     contexts.variable('family'),))
  
  fc_rule.fc_rule('classify_gruiforme_crane', This_rule_base, classify_gruiforme_crane,
    (('animals', 'candidate',
      (contexts.variable('bird_id'),),
      False),
     ('animals', 'bird_profile',
      (contexts.variable('bird_id'),
       contexts.anonymous('_'),
       contexts.anonymous('_'),
       pattern.pattern_literal('Gruiformes'),
       pattern.pattern_literal('Gruidae'),
       pattern.pattern_literal('wetland'),
       pattern.pattern_literal('omnivore'),
       pattern.pattern_literal('long_neck'),
       pattern.pattern_literal('very_large'),
       pattern.pattern_literal('migratory'),),
      False),),
    (pattern.pattern_literal('order'),
     pattern.pattern_literal('Gruiformes'),
     pattern.pattern_literal('family'),
     pattern.pattern_literal('Gruidae'),))


Krb_filename = '..\\src\\animal_expert_system\\knowledge\\animal_rules_fc.krb'
Krb_lineno_map = (
    ((12, 16), (7, 8)),
    ((17, 21), (9, 9)),
    ((22, 26), (10, 10)),
    ((27, 31), (11, 11)),
    ((32, 36), (12, 12)),
    ((37, 41), (13, 13)),
    ((42, 43), (15, 15)),
    ((44, 47), (16, 16)),
    ((56, 60), (21, 21)),
    ((61, 65), (22, 23)),
    ((66, 68), (25, 25)),
    ((69, 71), (26, 26)),
    ((80, 84), (31, 31)),
    ((85, 89), (32, 33)),
    ((90, 92), (35, 35)),
    ((93, 95), (36, 36)),
    ((104, 108), (41, 41)),
    ((109, 113), (42, 43)),
    ((114, 116), (45, 45)),
    ((117, 119), (46, 46)),
    ((128, 132), (51, 51)),
    ((133, 137), (52, 53)),
    ((138, 140), (55, 55)),
    ((141, 143), (56, 56)),
    ((152, 156), (61, 61)),
    ((157, 161), (62, 63)),
    ((162, 164), (65, 65)),
    ((165, 167), (66, 66)),
    ((176, 180), (71, 71)),
    ((181, 185), (72, 73)),
    ((186, 188), (75, 75)),
    ((189, 191), (76, 76)),
    ((200, 204), (81, 81)),
    ((205, 209), (82, 83)),
    ((210, 212), (85, 85)),
    ((213, 215), (86, 86)),
    ((224, 228), (91, 91)),
    ((229, 233), (92, 93)),
    ((234, 236), (95, 95)),
    ((237, 239), (96, 96)),
)
