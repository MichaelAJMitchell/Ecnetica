import random
import json
from sympy import symbols, sympify, latex, pi, simplify, factor, expand, sin, cos, sqrt

x, a, b, c, d, r_1, r_2 = symbols('x a b c d r_1 r_2')
local_namespace = {'x': x,'a':a,'b':b,'c':c, 'r_1': r_1, 'r_2': r_2,'sin': sin, 'cos': cos, 'pi': pi,'sqrt': sqrt}

def _generate_parameters(gen_defs):
    params ={}
    for name, rule in gen_defs['generated_parameters'].items():
        if rule['type']=='int':
            value = random.randint(rule['min'],rule['max'])
            if rule.get('exclude'):
                exclude = params[rule['exclude']]
                while value == exclude:
                    value = random.choice([i for i in range(rule['min'],rule['max']+1)if i != exclude])
        elif rule['type'] == 'choice':
            value = random.choice(rule['choices'])
        else:
            raise ValueError(f"Unknown type: {rule['type']}")
        params[name] = value

    return params
def generate_question_text(template):
    params = _generate_parameters(template['generated_parameters'])
    sympy_params = {k: sympify(v, locals=local_namespace) for k, v in params.items()}

    calc = {
    n: sympify(expr, locals=local_namespace).subs(params)
    for n, expr in template.get('calculated_parameters', {}).items()}

    all_syms = {**{k: sympify(v) for k,v in params.items()}, **calc}

    expr = sympify(template['question_expression'], locals=local_namespace).subs(all_syms)

    rendered_options = []
    for option in template['options']:
        if option in calc:
            val = calc[option]
        else:
            val = sympify(option, locals= local_namespace).subs({**sympy_params,**calc})
        rendered_options.append(latex(simplify(val)))


    # Format text
    if '${question_expression_subbed}$' in template['question_text']:
        q_text = template['question_text'].replace('${question_expression_subbed}$', f"${latex(expr)}$")
    else:
        q_text = template['question_template'].format(**params)

    return {
        'id': template['id'],
        'question': q_text,
        'options': rendered_options,
        'correct_index': template['correct_index'],
        'explanations': template.get('option_explanations', []),
        'params': params
    }

