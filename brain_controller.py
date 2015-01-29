from pybrain.structure import FeedForwardNetwork, RecurrentNetwork
from pybrain.structure import LinearLayer, SigmoidLayer, BiasUnit
from pybrain.structure import FullConnection
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from dataset import data
import pickle

class BrainController:

    indim = 2
    outdim = 2

    def __init__(self, trained_net = None):
        if trained_net == None:
            self.net = RecurrentNetwork()
            self.init_network(self.net)
        else:
            self.net = trained_net

    def init_network(self, net):
        net.addInputModule(LinearLayer(2, 'in'))
        net.addModule(SigmoidLayer(3, 'hidden'))
        net.addOutputModule(LinearLayer(2, 'out'))
        net.addModule(BiasUnit(name='bias'))
        net.addConnection(FullConnection(net['in'], net['hidden']))
        net.addConnection(FullConnection(net['hidden'], net['out']))
        net.sortModules()

    def train(self, data):
        ds = SupervisedDataSet(2, 2)
        for i in range(0, len(data)):
            input, target = data[i]
            ds.addSample(input, target)

        trainer = BackpropTrainer(self.net, ds, learningrate=0.01, momentum=0.99,
                verbose=True)

        max_error = 1e-5
        error = 1
        while abs(error) >= max_error:
            error = trainer.train()

        #self.validate_net()
        f = open('neuro.net', 'w')
        pickle.dump(self.net, f)
        f.close()

    def validate_net(self):
        print self.net.activate([0, 0])
        print self.net.activate([0, 1])
        print self.net.activate([0, 2])
        print self.net.activate([1, 0])
        print self.net.activate([1, 1])
        print self.net.activate([1, 2])


#brain = BrainController()
#brain.train(data*1000)
#brain.validate_net()
