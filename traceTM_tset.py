## Project 02 -- Tracing Nondeterministic Turing Machines
## Carlos Basurto
## Theory of Computing
## 12/06/24

# Libraries

import statistics
import sys

## Nondeterministic Turing Machine Class
class NTM:

    # Initialize the 8-tuple with the provided parameters
    def __init__(self, name, states, input_alph, tape_alph, starting_q, accept_q, reject_q, transitions):
        self.name        = name
        self.states      = states
        self.input_alph  = input_alph
        self.tape_alph   = tape_alph
        self.starting_q  = starting_q
        self.accept_q    = accept_q
        self.reject_q    = reject_q
        self.transitions = transitions

    # Print NTM cleanly
    def __str__(self):
        return f"NTM {self.name}:\n  States: {self.states}\n  Input Alphabet: {self.input_alph}\n  Tape Alphabet: {self.tape_alph}\n  Starting State: {self.starting_q}\n  Accept State: {self.accept_q}\n  Reject State: {self.reject_q}\n  Transition Table: {self.transitions}\n"
    
    # Run the NTM on a provided input and a set max depth
    def run(self, input, max_depth):

        print(f"Running {self.name} on string {input[:-1]}")

        accepted = False

        tapes          = []
        configurations = []

        # Append initial tape and configuration
        tapes.append([input, self.starting_q, 0, 0])
        configurations.append(["", self.starting_q, input])

        while tapes:

            # Current state of the tape, string and head position
            curr = tapes.pop()

            # For a given position in the tape, attempt every transition
            for transition in self.transitions:
                string = curr[0]
                state  = curr[1]
                head   = int(curr[2])
                depth  = int(curr[3]) + 1

                # If depth is exceeped, halt operation
                if (depth > max_depth):
                    tapes.clear()
                    break 
                
                # If there is a match in the state and input character, realize the transition
                if (state == transition[0]) and (string[head] == transition[1]):
                    new_state  = transition[2]
                    string = string[:head] + transition[3] + string[head+1:]
                    head = head + 1 if transition[4] == 'R' else head - 1

                    # Ensure head is within limits
                    if head < 0:
                        head = 0 
                    elif head >= len(string):
                        string += "_"

                    configurations.append([string[:head], new_state, string[head:]])

                    # If end state is reached, halt branch
                    if new_state == self.accept_q:
                        accepted = True
                        continue
                    elif new_state == self.reject_q:
                        continue

                    tapes.append([string, new_state, head, depth])

        # Sort configurations by depth
        configurations = sorted(configurations, key=lambda x: (len([x]), x[0]))

        d      = 0
        level  = 0
        levels = []
        
        # Print configurations by depth
        for configuration in configurations:
            if len(configuration[0]) != d:
                d += 1
                print("")
                levels.append(level)
                level = 0
            print(f"| {configuration[0]}, {configuration[1]}, {configuration[2]} ", end="")
            level += 1

        if (depth > max_depth):
            print("\nDepth limit exceeded", end="")

        nondeterminism = statistics.mean(levels) if levels else 1

        # Return acceptance status, depth, and nondeterminism level
        return accepted, d, nondeterminism

# Read the NTM described in the provided csv files
def read_ntm(file_path):

    with open(file_path, 'r') as file:
        transitions = []
        
        for i, line in enumerate(file):
            if (i == 0):
                name = line.strip()
            elif (i == 1):
                states = []
                for state in line.strip().split(","):
                    states.append(state)
            # For alphabets, characters are appended individually
            elif (i == 2):
                input_alph = []
                for char in line.strip().split(","):
                    input_alph.append(char)
            elif (i == 3):
                tape_alph = []
                for char in line.strip().split(","):
                    tape_alph.append(char)
            if (i == 4):
                starting_q = line.strip()
            if (i == 5):
                accept_q = line.strip()
            if (i == 6):
                reject_q = line.strip()
            # All subsequent lines are transitions
            if (i > 6):
                transition = line.strip().split(",")
                transitions.append(transition)

        # Return initialized NTM with the provided information
        return NTM(name, states, input_alph, tape_alph, starting_q, accept_q, reject_q, transitions)


# Iterate through files in the folder
for file_name in ['a_plus.csv', 'abc_star.csv']:
    with open(file_name[:-4]+'_inputs.txt') as inputs, open(file_name[:-4]+'_outputs.txt', 'w') as output:
            
            # Initialize NTM
            ntm = read_ntm(file_name)

            # Redirect output
            original_stdout = sys.stdout
            sys.stdout = output

            try:
                # Print NTM 
                print(ntm)

                # Run a set of inputs on the NTM            
                for input_string in inputs:

                    accepted, depth, nondetermism = ntm.run(input_string.rstrip()+'_', 10)

                    # Print run results
                    if (accepted):
                        print(f"\nString {input_string.rstrip()} accepted in {depth} transitions with a nondeterminism of: {nondetermism}\n")
                    else:
                        print(f"\nString {input_string.rstrip()} rejected in {depth} transitions with a nondeterminism of: {nondetermism}\n")
            finally:
                # Restore stdout
                sys.stdout = original_stdout