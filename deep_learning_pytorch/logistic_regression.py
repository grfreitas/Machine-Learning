
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_points(X, y):
    admitted = X[np.argwhere(y==1)]
    rejected = X[np.argwhere(y==0)]
    plt.scatter([s[0][0] for s in rejected], [s[0][1] for s in rejected], s = 25, color = 'blue', edgecolor = 'k')
    plt.scatter([s[0][0] for s in admitted], [s[0][1] for s in admitted], s = 25, color = 'red', edgecolor = 'k')

def display(m, b, epoch, accuracy, color='g--'):
    plt.xlim(-.5,1.5)
    plt.ylim(-.5,1.5)
    x = np.arange(-10, 10, 0.1)
    plt.title('Num Epochs: {} | Epoch: {} | Learning Rate: {} | Accuracy: {}'.format(epochs, epoch+1, learnrate, round(accuracy,4)))
    plt.plot(x, m*x+b, color, alpha=np.linspace(0,1,epochs)[epoch])

data = pd.read_csv('data.csv', header=None)
X = np.array(data[[0,1]])
y = np.array(data[2])
plt.figure(figsize=(10,10))
plot_points(X,y)

# Activation (sigmoid) function
def sigmoid(x):
    return 1/(1+np.exp(-x))

# Output (prediction) formula
def output_formula(features, weights, bias):
    y_hat = sigmoid(np.matmul(features,weights) + bias)
    return y_hat

# Error (log-loss) formula
def error_formula(y, output):
    error = -y*np.log(output)-(1-y)*np.log(1-output)
    return error

# Gradient descent step
def update_weights(x, y, weights, bias, learnrate):

    y_hat = output_formula(x, weights, bias)
    
    weights = weights + learnrate*(y-y_hat)*x
    bias    = bias    + learnrate*(y-y_hat)
    
    return weights, bias

np.random.seed(120)
epochs = 100
learnrate = 0.01

def train(features, targets, epochs, learnrate, graph_lines=False):

    errors = []
    n_records, n_features = features.shape
    last_loss = None
    weights = np.random.normal(scale=1/n_features**.5, size=n_features)
    bias = 0
    for e in range(epochs):
        del_w = np.zeros(weights.shape)
        for x, y in zip(features, targets):
            output = output_formula(x, weights, bias)
            error = error_formula(y, output)
            weights, bias = update_weights(x, y, weights, bias, learnrate)
        
        # Printing out the log-loss error on the training set
        out = output_formula(features, weights, bias)
        loss = np.mean(error_formula(targets, out))
        errors.append(loss)
        if e % (epochs / 10) == 0:
            print("\n========== Epoch", e,"==========")
            if last_loss and last_loss < loss:
                print("Train loss: ", loss, "  WARNING - Loss Increasing")
            else:
                print("Train loss: ", loss)
            last_loss = loss
            predictions = out > 0.5
            accuracy = np.mean(predictions == targets)
            print("Accuracy: ", accuracy)
        if graph_lines and e % (epochs / 100) == 0:
            display(-weights[0]/weights[1], -bias/weights[1], e, accuracy)
            plt.pause(0.1)

    # Plotting the solution boundary
    display(-weights[0]/weights[1], -bias/weights[1], e, accuracy, 'black')
    plt.pause(0.2)
    plt.show()

    # # Plotting the error
    # plt.title("Error Plot")
    # plt.xlabel('Number of epochs')
    # plt.ylabel('Error')
    # plt.plot(errors)
    # plt.show()

train(X, y, epochs, learnrate, True)