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

# Weight parameters (tunable)
alpha = np.array([0.5, 0.3, 0.1, 0.1, 0.0])
gamma = np.array([0.2]*dim)
theta = np.array([1.0, 1.0, 1.0, 0.5, 0.5])
beta = 0.8
delta = 0.9

# Environment / reality function
def reality_function(A):
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

# --- Mastery principle: compute optimal action ---
def compute_optimal_action(C, W, M, F, P, candidate_actions):
    phi_values = np.array([phi_alignment(C, W, M, k_feedback(A, reality_function(A)), P) for A in candidate_actions])
    A_star = candidate_actions[np.argmax(phi_values)]
    return A_star

# --- Generate candidate detours ---
def generate_detours(A, num_detours=5, scale=0.1):
    # Slight random variations around A
    detours = [A + np.random.uniform(-scale, scale, size=A.shape) for _ in range(num_detours)]
    return detours + [A]  # Include original action as candidate

# --- Iterative loop ---
time_steps = 100
dt = 1.0

for t in range(time_steps):
    # 1. Compute beneficence (integrated moral work)
    B += h_action(I, W, M, C, R) * dt

    # 2. Compute instantaneous trajectory (mercy)
    R = (h_action(I, W, M, C, R) - B)/dt

    # 3. Generate base action
    A_base = h_action(I, W, M, C, R)

    # 4. Mastery principle: generate candidate detours and select optimal action
    candidates = generate_detours(A_base)
    A = compute_optimal_action(C, W, M, F=np.zeros_like(A_base), P=P, candidate_actions=candidates)

    # 5. Apply feedback
    F = k_feedback(A, reality_function(A))

    # 6. Update moral anchor
    M += lambda_ * F

    # 7. Update consciousness
    C += f_consciousness(I, W, M, B)
    C *= E

    # 8. Update watchfulness
    W = g_watchfulness(C)

    # 9. Compute alignment projection
    L = projection(C, M)

    # 10. Compute accountability
    Q = np.sum(np.abs(F))

    # 11. Update purpose (tangent of moral trajectory)
    P = compute_tangent(B, R)

    # Optional: print state
    print(f"Step {t}: C={C}, W={W:.3f}, M={M}, B={B}, R={R}, L={L:.3f}, P={P}, A={A}")
