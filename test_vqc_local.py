"""Quick local test of VQC training to find the actual error."""
import sys
sys.path.insert(0, "Diseases_Detection_Paltform/backend")

import numpy as np

try:
    from app.ml.quantum.vqc.model import VariationalQuantumClassifier
    print("VQC import OK")
    
    # Simulate 4-feature binary classification (like Lung Cancer dataset)
    np.random.seed(42)
    X_train = np.random.rand(20, 4)  # 20 samples, 4 features
    y_train = np.random.randint(0, 2, 20)
    X_test = np.random.rand(5, 4)
    
    print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
    
    vqc = VariationalQuantumClassifier(
        n_qubits=4, n_layers=2, epochs=1, batch_size=8,
        lr=0.03, encoding_method="angle_ry", variational_gate="RY",
        entanglement_strategy="linear_cnot"
    )
    print("VQC created OK")
    
    print("Starting fit...")
    vqc.fit(X_train, y_train)
    print("Fit completed OK!")
    
    probs = vqc.predict_proba(X_test)
    print(f"Predictions: {probs}")
    print("SUCCESS - VQC works locally")
    
except Exception as e:
    import traceback
    print(f"FAILED: {e}")
    traceback.print_exc()
