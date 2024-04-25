import numpy as np
import matplotlib.pyplot as plt

class PerceptronLearning:
    def __init__(self, input_size, alpha = 1):
        self.alpha = alpha
        self.weights = np.zeros(input_size + 1)

    def predict(self, inputs):
        activation = np.dot(inputs, self.weights[1:]) + self.weights[0]
        if (activation >= 0):
           return 1
        else:
           return 0

    def train(self, inputs, labels, epochs=100):
        for _ in range(epochs):
            weights_updated = False
            for x, y in zip(inputs, labels):
                y_pred = self.predict(x)
                error = y - y_pred
                if (error != 0):
                     self.weights[1:] += self.alpha * error * x
                     self.weights[0] += self.alpha * error
                     weights_updated = True
            if not weights_updated:
                break

X_train = np.array([[1, 0, 0], [0, 1, 1], [1, 1, 0], [1, 1, 1], [0, 0, 1], [1, 0, 1]])
y_train = np.array([1, 0, 1, 0, 0, 1])
p = PerceptronLearning(input_size = 3, alpha = 1)
p.train(X_train, y_train)
for i, x in enumerate(X_train):
    print("Example", (i+1), "Inputs:", x, "-> Output:", p.predict(x))
print("Final Weights:", p.weights)

plt.plot(p.weights)
plt.title("Weight Vector")
plt.xlabel("Index")
plt.ylabel("Weight Value")
plt.show()