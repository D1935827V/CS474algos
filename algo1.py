from automata.fa.dfa import DFA
# I used https://pypi.org/project/automata-lib/ to simulate the DFAs in this algorithim, Assistance to Author West Point NY 14MAR2025

def is_multiple_of_13(dfa):
    
    #DFA for multiples of 13
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
    
    compliment_dfa = ~dfa
    intersection1 = compliment_dfa.intersection(dfa_multiples_of_13)
    is_valid = intersection1.isempty()
    
    return is_valid


#DFA that accepts all base 3 numbers
dfa_all_base3 = DFA(
    states={'q0'},
    input_symbols={'0', '1', '2'},
    transitions={
        'q0': {'0': 'q0', '1': 'q0', '2': 'q0'}
    },
    initial_state='q0',
    final_states={'q0'}
)

#DFA that accepts base 3 multiples of 13
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

#DFA that rejects 111
dfa_rejects_111 = DFA(
    states={'q0', 'q1'},
    input_symbols={'0', '1', '2'},
    transitions={
        'q0': {'0': 'q0', '1': 'q1', '2': 'q0'},
        'q1': {'0': 'q1', '1': 'q0', '2': 'q1'}
    },
    initial_state='q0',
    final_states={'q0'}
)

print(is_multiple_of_13(dfa_all_base3))
print(is_multiple_of_13(dfa_multiples_of_13))
print(is_multiple_of_13(dfa_rejects_111))


import time
import random
import matplotlib.pyplot as plt

def generate_random_dfa(num_states, alphabet={'0', '1', '2'}) -> DFA:
    states = {f'q{i}' for i in range(num_states)}
    state_list = list(states)
    transitions = {}

    for state in states:
        transitions[state] = {}
        for symbol in alphabet:
            transitions[state][symbol] = random.choice(state_list)

    initial_state = 'q0'
    final_states = set(random.sample(state_list, k=random.randint(1, max(1, num_states // 10))))

    return DFA(
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
    dfa = generate_random_dfa(size)
    start = time.perf_counter()
    try:
        is_multiple_of_13(dfa)
    except Exception as e:
        print(f"Error at size {size}: {e}")
    end = time.perf_counter()
    elapsed = end - start
    times.append(elapsed)
    print(f"DFA with {size} states took {elapsed:.4f} seconds.")

# Plotting results
plt.figure(figsize=(10, 6))
plt.plot(sizes, times, marker='o')
plt.title('is_multiple_of_13 Runtime vs DFA Size')
plt.xlabel('Number of States in DFA')
plt.ylabel('Time (seconds)')
plt.grid(True)
plt.tight_layout()
plt.show()
