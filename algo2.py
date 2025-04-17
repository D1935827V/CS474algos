from automata.fa.nfa import NFA
from automata.fa.dfa import DFA

#nfa to dfa conversion takes exponential time
def check_nfa_acceptance(nfa):
    dfa_multiples_of_13 = DFA(
        states={'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'},
        input_symbols={'0', '1', '2'},
        transitions={
            '0': {'0': '0', '1': '1', '2': '2'},
            '1': {'0': '3', '1': '4', '2': '5'},
            '2': {'0': '6', '1': '7', '2': '8'},
            '3': {'0': '9', '1': '10', '2': '11'},
            '4': {'0': '12', '1': '0', '2': '1'},
            '5': {'0': '2', '1': '3', '2': '4'},
            '6': {'0': '6', '1': '7', '2': '8'},
            '7': {'0': '9', '1': '10', '2': '11'},
            '8': {'0': '12', '1': '0', '2': '1'},
            '9': {'0': '3', '1': '4', '2': '5'},
            '10': {'0': '6', '1': '7', '2': '8'},
            '11': {'0': '9', '1': '10', '2': '11'},
            '12': {'0': '12', '1': '0', '2': '1'}
        },
        initial_state='0',
        final_states={'0'}
    )

    dfa = DFA.from_nfa(nfa)

    # Fix for garbage collection issue
    compliment_dfa = ~dfa
    intersection1 = compliment_dfa.intersection(dfa_multiples_of_13)
    is_valid = not intersection1.isempty()

    intersection2 = dfa.intersection(~dfa_multiples_of_13)
    finite = intersection2.isfinite()

    return not is_valid, finite




nfa_all_base3 = NFA(
    states={'q0'},
    input_symbols={'0', '1', '2'},
    transitions={
        'q0': {'0': {'q0'}, '1': {'q0'}, '2': {'q0'}}
    },
    initial_state='q0',
    final_states={'q0'}
)

nfa_multiples_of_13 = NFA(
        states={'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'},
        input_symbols={'0', '1', '2'},
        transitions={
            '0': {'0': {'0'}, '1': {'1'}, '2': {'2'}},
            '1': {'0': {'3'}, '1': {'4'}, '2': {'5'}},
            '2': {'0': {'6'}, '1': {'7'}, '2': {'8'}},
            '3': {'0': {'9'}, '1': {'10'}, '2': {'11'}},
            '4': {'0': {'12'}, '1': {'0'}, '2': {'1'}},
            '5': {'0': {'2'}, '1': {'3'}, '2': {'4'}},
            '6': {'0': {'6'}, '1': {'7'}, '2': {'8'}},
            '7': {'0': {'9'}, '1': {'10'}, '2': {'11'}},
            '8': {'0': {'12'}, '1': {'0'}, '2': {'1'}},
            '9': {'0': {'3'}, '1': {'4'}, '2': {'5'}},
            '10': {'0': {'6'}, '1': {'7'}, '2': {'8'}},
            '11': {'0': {'9'}, '1': {'10'}, '2': {'11'}},
            '12': {'0': {'12'}, '1': {'0'}, '2': {'1'}}
        },
        initial_state='0',
        final_states={'0'}
)

nfa_rejects_111 = NFA(
    states={'q0', 'q1'},
    input_symbols={'0', '1', '2'},
    transitions={
        'q0': {'0': {'q0'}, '1': {'q1'}, '2': {'q0'}},
        'q1': {'0': {'q1'}, '1': {'q0'}, '2': {'q1'}}
    },
    initial_state='q0',
    final_states={'q0'}
)

nfa_finite = NFA(
    states={'q0', 'q1', 'q2', 'dead'},
    input_symbols={'0', '1', '2'},
    transitions={
        'q0': {'0': {'q1'}, '1': {'q2'}, '2': {'dead'}},
        'q1': {'0': {'dead'}, '1': {'dead'}, '2': {'dead'}},
        'q2': {'0': {'dead'}, '1': {'dead'}, '2': {'dead'}},
        'dead': {'0': {'dead'}, '1': {'dead'}, '2': {'dead'}}
    },
    initial_state='q0',
    final_states={'q1', 'q2'}
)

print(check_nfa_acceptance((nfa_all_base3))) #true false
print(check_nfa_acceptance((nfa_multiples_of_13))) #true true
print(check_nfa_acceptance((nfa_rejects_111))) #false false
print(check_nfa_acceptance((nfa_finite))) #false true

import random
import time
import matplotlib.pyplot as plt

def generate_random_nfa(num_states, alphabet={'0', '1', '2'}) -> NFA:
    states = {f'q{i}' for i in range(num_states)}
    transitions = {}
    for state in states:
        transitions[state] = {}
        for symbol in alphabet:
            # Choose 1-3 random target states for each symbol
            transitions[state][symbol] = set(random.choices(list(states), k=random.randint(1, 3)))
    initial_state = 'q0'
    final_states = set(random.sample(list(states), k=random.randint(1, max(1, num_states // 10))))
    return NFA(
        states=states,
        input_symbols=alphabet,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states
    )

# Settings for benchmark
sizes = list(range(10, 220, 30))  # 10, 40, ..., 280
times = []

for size in sizes:
    nfa = generate_random_nfa(size)
    start = time.perf_counter()
    try:
        check_nfa_acceptance(nfa)
    except Exception as e:
        print(f"Error at size {size}: {e}")
    end = time.perf_counter()
    times.append(end - start)
    print(f"NFA with {size} states took {times[-1]:.4f} seconds.")

# Plotting results
plt.figure(figsize=(10, 6))
plt.plot(sizes, times, marker='o')
plt.title('check_nfa_acceptance Runtime vs NFA Size')
plt.xlabel('Number of States in NFA')
plt.ylabel('Time (seconds)')
plt.grid(True)
plt.tight_layout()
plt.show()
