from utils.network import Network
import numpy as np
import copy


class Genome(object):
    def __init__(self, network_params, mutation_rate, mutation_scale, parent_1=None, parent_2=None):
        # fitness is score normalized
        self.fitness = 0
        self.score = 0

        # keep track of how genome came to be
        self.mutated = False
        self.bred = False

        self.inputs = network_params['input']
        self.hidden = network_params['hidden']
        self.outputs = network_params['output']

        self.mutation_rate = mutation_rate
        self.mutation_scale = mutation_scale

        self.weights = None
        self.biases = None

        # two parents available for breeding
        if parent_2 is not None:
            self.weights = copy.deepcopy(parent_1.weights)
            self.biases = copy.deepcopy(parent_1.biases)
            self.breed(parent_2)
            self.bred = True

        # mutate if only one parent available
        elif parent_1 is not None:
            self.weights = copy.deepcopy(parent_1.weights)
            self.biases = copy.deepcopy(parent_1.biases)
            self.mutate()
            self.mutated = True

        # initial values when population is first created
        else: self.init_w_b()

        # pass genome to network object
        self.model = Network(self)

    def init_w_b(self):
        # create weights and bias for first hidden layer
        self.weights = [np.random.randn(self.inputs, self.hidden[0]).astype(np.float32)]
        self.biases = [np.random.rand(self.hidden[0]).astype(np.float32)]

        # if there are additional hidden layers
        for i in range(len(self.hidden) - 1):
            self.weights.append(np.random.randn(self.hidden[i], self.hidden[i+1]).astype(np.float32))
            self.biases.append(np.random.randn(self.hidden[i+1]).astype(np.float32))

        # weights for last layer
        self.weights.append(np.random.randn(self.hidden[-1], self.outputs).astype(np.float32))
        self.biases.append(np.random.randn(self.outputs).astype(np.float32))

    def mutate(self):
        # iterate through layers
        for i, layers in enumerate(self.weights):
            for (j, k), x in np.ndenumerate(layers):

                # randomly mutate based on mutation rate
                if np.random.random() < self.mutation_rate:
                    self.weights[i][j][k] += np.random.normal(scale=self.mutation_scale) * 0.5

    def breed(self, parent):
        # iterate through layers
        for i, layers in enumerate(self.weights):
            for (j, k), x in np.ndenumerate(layers):
                # equal chance of weight being from each parent
                if np.random.random() > 0.5:
                    self.weights[i][j][k] = parent.weights[i][j][k]