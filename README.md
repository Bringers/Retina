# Retina
A machine learning project using STDP neurons in a spiking network to learn and distinguish right and left 1-dimensional motion.

You can choose to train your own network or use the already trained model with 1000 neurons trained over night.
The network is a shallow network using spiking neurons and STDP to learn.

The network performs very well when using the camera but not alot of time has been put into hyperparameter optimization.

# Input
The input is a strip from top to bottom with a new row of pixels generated every time step. The width of the image is 255 pixels. In order to be similar to the real data the datagenerator generates some noice instead of a clean line.
![Different input images](https://i.imgur.com/AZnBM07.png)
![Camera input](https://i.imgur.com/i6L4CXd.png)

# The model
The model has only two hidden layers with an excitatory and an inhibitory layer. The inhibition from the inhibitory layer creates a "winner takes all" situation where the strong excitatory neurons become representative of the input. The excitatory layer is then mapped to the output layer depending on which direction the neuron spiked the most.
![The model](https://i.imgur.com/83vFbpa.png)
![Map to output](https://i.imgur.com/9Vmnlug.png)

# Training
The training was setup so that the network trained on one direction for half the time, letting the inhibition do it's work, and then swap to the other direction. The representative neurons can clearly be seen when training on 1000 neurons.
![Training](https://i.imgur.com/fafNuZi.png)
