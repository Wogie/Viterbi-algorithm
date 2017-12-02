import viterbi_module as vit
import matplotlib.pyplot as plt

myparams = vit.ViterbiParams()

my_throws, my_states = vit.simulate_throws(myparams.transition_probs, myparams.emissionprobs, number=300)

most_prob_path, my_vit_materix = vit.viterbi(my_throws, myparams)

print(my_vit_materix)
print(my_throws)
print(my_states)
print(most_prob_path)

# Plotting correct estimates
plt.axis([0, len(my_throws), 9, 11])
for i in range(len(my_throws)):
    if (i / 10).is_integer():
        print(i)
    if my_states[i] == 'loaded' and most_prob_path[i] == 'loaded':
        plt.plot(i + 2, 10, 'go')
    elif my_states[i] == 'loaded' and most_prob_path[i] == 'fair':
        plt.plot(i + 2, 10, 'ro')
    elif my_states[i] == 'fair' and most_prob_path[i] == 'loaded':
        plt.plot(i + 2, 10, 'bo')

# Green indicates that viterbi correclty guessed loaded (hard)
# Red indicates that viterbi didn't detect loaded
# Blue indicates that viterbi guessed loaded even though it wasn't
# Everywhere else, both are fair

# Making csv file
for i in [1]:
    my_throws = [str(i) for i in my_throws]

    my_throws.insert(0, 'throw')
    my_states.insert(0, 'state')
    most_prob_path.insert(0, "Viterbi")

    csv1 = ";".join(my_throws)
    csv2 = ";".join(my_states)
    csv3 = ";".join(most_prob_path)

    csv = "\n".join((csv1, csv2, csv3))

    with open('viterbi_predictions.csv', 'w') as f:
        f.write(csv)

    print(csv)

plt.savefig("my_viterbi_estimation_rolls.png")
