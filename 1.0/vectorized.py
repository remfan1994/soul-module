import numpy as np

# --- Initialization ---
dim = 5  # Dimensionality of consciousness/moral vectors

C = np.ones(dim) * 1.0      # Consciousness capital vector
W = 0.5                     # Watchfulness scalar
M = np.ones(dim) * 1.0      # Moral anchor vector
I = np.ones(dim) * 0.7      # Intention vector
B = np.zeros(dim)            # Beneficence (integrated work vector)
R = np.zeros(dim)            # Mercy (instantaneous slope vector)
P = np.zeros(dim)            # Purpose / trajectory vector
E = 1.1                     # Elevation scaling factor
lambda_ = 0.1               # Feedback learning rate

# Optional triangulated elements
L = 0.0                     # Alignment projection scalar
Q = 0.0                     # Accountability weight scalar

# Weight parameters (can be tuned)
alpha = np.array([0.5, 0.3, 0.1, 0.1, 0.0])
gamma = np.array([0.2]*dim)
theta = np.array([1.0, 1.0, 1.0, 0.5, 0.5])
beta = 0.8
delta = 0.9

# Placeholder for environment / reality function
def reality_function(A):
    # Environment slightly modifies the action vector
    noise = np.random.uniform(0.95, 1.05, size=A.shape)
    return A * noise

# --- Function definitions ---
def f_consciousness(I, W, M, B):
    return alpha[0]*I + alpha[1]*W + alpha[2]*M + alpha[3]*B + alpha[4]*np.zeros_like(B)

def g_watchfulness(C):
    return beta * np.log(1 + np.linalg.norm(C))

def h_action(I, W, M, C, R):
    return gamma[0]*I + gamma[1]*W + gamma[2]*M + gamma[3]*C + gamma[4]*R

def k_feedback(A, Reality):
    return delta * (Reality - A)

def phi_alignment(C, W, M, F, P):
    return theta[0]*np.linalg.norm(C) + theta[1]*W + theta[2]*np.linalg.norm(M) - theta[3]*np.linalg.norm(F) + theta[4]*np.linalg.norm(P)

def projection(C, M):
    return np.dot(C, M) / (np.linalg.norm(C)*np.linalg.norm(M) + 1e-9)

def compute_tangent(B, R):
    slope = R
    norm = np.linalg.norm(slope) + 1e-9
    return slope / norm

# --- Iterative loop ---
time_steps = 100
dt = 1.0

for t in range(time_steps):
    # 1. Compute beneficence (integrated moral work)
    B += h_action(I, W, M, C, R) * dt

    # 2. Compute instantaneous trajectory (mercy)
    R = (h_action(I, W, M, C, R) - B)/dt

    # 3. Generate action
    A = h_action(I, W, M, C, R)

    # 4. Apply feedback
    F = k_feedback(A, reality_function(A))

    # 5. Update moral anchor
    M += lambda_ * F

    # 6. Update consciousness
    C += f_consciousness(I, W, M, B)
    C *= E

    # 7. Update watchfulness
    W = g_watchfulness(C)

    # 8. Compute alignment projection
    L = projection(C, M)

    # 9. Compute accountability (sum of absolute feedbacks)
    Q = np.sum(np.abs(F))

    # 10. Update purpose (tangent of moral trajectory)
    P = compute_tangent(B, R)

    # Optional: print state at each step
    print(f"Step {t}: C={C}, W={W:.3f}, M={M}, B={B}, R={R}, L={L:.3f}, P={P}")
