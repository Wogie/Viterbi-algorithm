import numpy as np
import random


def simulate_throws(transition_probs, emissionprobs, number=10):
    dice_eyes = [1, 2, 3, 4, 5, 6]
    states = ["fair", "loaded"]
    first_state = random.choices(states, transition_probs["fair"])[0]

    throws = []
    throw_states = [first_state]

    current_state = first_state

    for i in range(0, number):
        if current_state == "fair":
            throw = random.choices(dice_eyes, emissionprobs["fair"])[0]
            throws.append(throw)
            if i != number - 1:
                current_state = random.choices(states, transition_probs["fair"])[0]
                throw_states.append(current_state)
            else:
                break
        elif current_state == "loaded":
            throw = random.choices(dice_eyes, emissionprobs["loaded"])[0]
            throws.append(throw)
            if i != number - 1:
                current_state = random.choices(states, transition_probs["loaded"])[0]
                throw_states.append(current_state)
            else:
                break

    return throws, throw_states


class ViterbiParams:
    def __init__(self):
        self.state_names = ['fair', 'loaded']

        self.loaded_to_fair = 0.1
        self.loaded_to_loaded = 0.9
        self.fair_to_fair = 0.95
        self.fair_to_loaded = 0.05

        self.transition_probs = {"fair": [self.fair_to_fair, self.fair_to_loaded],
                                 "loaded": [self.loaded_to_fair, self.loaded_to_loaded]}

        self.fair_emmisions = [1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6]
        self.loaded_emmisions = [1 / 10, 1 / 10, 1 / 10, 1 / 10, 1 / 10, 1 / 2]

        self.emissionprobs = {"fair": self.fair_emmisions, "loaded": self.loaded_emmisions}


def viterbi(throws_sim, paraobjct):
    state_names = paraobjct.state_names
    transition_probs = paraobjct.transition_probs
    emissionprobs = paraobjct.emissionprobs

    viterbi_matrix = np.array(np.zeros(shape=(len(state_names) + 2, len(throws_sim) + 1)))

    viterbi_matrix[0, 0] = 1

    # Viterbi algorithm
    for i in range(len(throws_sim)):

        for j in range(len(state_names)):
            # from 0
            choice1 = viterbi_matrix[0, i] * transition_probs[state_names[0]][j]
            # from 1
            choice2 = viterbi_matrix[1, i] * transition_probs[state_names[0]][j]
            # from 2
            choice3 = viterbi_matrix[2, i] * transition_probs[state_names[1]][j]

            choice = max(choice1, choice2, choice3)

            if j == 0:
                if choice == choice1 or choice == choice2:
                    viterbi_matrix[0, i + 1] = 0
                elif choice == choice3:
                    viterbi_matrix[0, i + 1] = 1

            elif j == 1:
                if choice == choice1 or choice == choice2:
                    viterbi_matrix[3, i + 1] = 0
                elif choice == choice3:
                    viterbi_matrix[3, i + 1] = 1

            calculation = choice
            emission = emissionprobs[state_names[j]]
            emission = emission[throws_sim[i] - 1]
            calculation = calculation * emission
            viterbi_matrix[j + 1, i + 1] = calculation

    # Backtracing
    optimal_path_current = max((viterbi_matrix[1, -1], viterbi_matrix[2, -1]))

    if optimal_path_current == viterbi_matrix[1, -1]:
        optimal_path_current = 'fair'
    else:
        optimal_path_current = 'loaded'

    most_probable_path = [optimal_path_current]

    for i in range(2, len(throws_sim) + 1):
        if optimal_path_current == 'fair':
            if viterbi_matrix[0, -(i - 1)] == 0:
                optimal_path_current = 'fair'
            elif viterbi_matrix[0, -(i - 1)] == 1:
                optimal_path_current = 'loaded'

        elif optimal_path_current == 'loaded':
            if viterbi_matrix[3, -(i - 1)] == 0:
                optimal_path_current = 'fair'
            elif viterbi_matrix[3, -(i - 1)] == 1:
                optimal_path_current = 'loaded'

        most_probable_path.insert(0, optimal_path_current)

    return most_probable_path, viterbi_matrix
