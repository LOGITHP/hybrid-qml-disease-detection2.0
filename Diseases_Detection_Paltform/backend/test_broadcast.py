import pennylane as qml
from pennylane import numpy as pnp
import numpy as np

n_qubits = 4
n_layers = 2
device_name = "default.qubit"

dev = qml.device(device_name, wires=n_qubits)

@qml.qnode(dev)
def circuit(x, weights):
    for i in range(n_qubits):
        qml.RY(x[..., i] * pnp.pi, wires=i)
    for l in range(n_layers):
        for i in range(n_qubits):
            qml.RY(weights[l, i], wires=i)
        for i in range(n_qubits - 1):
            qml.CNOT(wires=[i, i + 1])
    return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]

batch_size = 5
X = pnp.random.random((batch_size, n_qubits))
weights = pnp.random.random((n_layers, n_qubits))

res = circuit(X, weights)
print("Res type:", type(res))
if isinstance(res, tuple):
    print("Res length:", len(res))
    print("Element shape:", res[0].shape)
    
stacked = pnp.stack(res)
print("Stacked shape:", stacked.shape)
mean = pnp.mean(stacked, axis=0)
print("Mean shape:", mean.shape)
