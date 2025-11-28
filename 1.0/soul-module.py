import numpy as np
from scipy.integrate import cumtrapz
from scipy.misc import derivative

# --- Initialization ---
dim = 5
time_steps = 100
dt = 0.1
times = np.linspace(0, (time_steps-1)*dt, time_steps)

C = np.ones(dim) * 1.0
W = 0.5
M = np.ones(dim) * 1.0
I = np.ones(dim) * 0.7
B = np.zeros((time_steps, dim))
R = np.zeros((time_steps, dim))
P = np.zeros(dim)
E = 1.1
lambda_ = 0.1

# Weight parameters
alpha = np.array([0.5, 0.3, 0.1, 0.1, 0.0])
gamma = np.array([0.2]*dim)
theta = np.array([1.0, 1.0, 1.0, 0.5, 0.5])
beta = 0.8
delta = 0.9

# --- Environment / reality function ---
def reality_function(A):
    noise = np.random.uniform(0.95, 1.05, size=A.shape)
    return A * noise

# --- Core functions ---
def f_consciousness(I, W, M, B_vector):
    return alpha[0]*I + alpha[1]*W + alpha[2]*M + alpha[3]*B_vector + alpha[4]*np.zeros_like(B_vector)

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

def compute_tangent(B_vector, R_vector):
    slope = R_vector
    norm = np.linalg.norm(slope) + 1e-9
    return slope / norm

# Mastery principle
def compute_optimal_action(C, W, M, F, P, candidate_actions):
    phi_values = np.array([phi_alignment(C, W, M, k_feedback(A, reality_function(A)), P) for A in candidate_actions])
    return candidate_actions[np.argmax(phi_values)]

def generate_detours(A, num_detours=5, scale=0.1):
    detours = [A + np.random.uniform(-scale, scale, size=A.shape) for _ in range(num_detours)]
    return detours + [A]

# --- Iterative loop with continuous integration ---
actions_history = []

for t in range(time_steps):
    # 1. Compute current action
    A_base = h_action(I, W, M, C, R[t-1] if t>0 else np.zeros(dim))

    # 2. Generate candidate detours and select optimal action
    candidates = generate_detours(A_base)
    A = compute_optimal_action(C, W, M, F=np.zeros(dim), P=P, candidate_actions=candidates)

    # 3. Store action
    actions_history.append(A)

    # 4. Compute continuous beneficence using trapezoidal integration
    if t == 0:
        B[t] = A * dt
    else:
        B[t] = cumtrapz(np.array(actions_history), times[:t+1], axis=0, initial=0)[-1]

    # 5. Compute continuous derivative for mercy
    if t == 0:
        R[t] = np.zeros(dim)
    else:
        R[t] = np.gradient(B[:t+1], axis=0)[-1] / dt

    # 6. Apply feedback
    F = k_feedback(A, reality_function(A))

    # 7. Update moral anchor
    M += lambda_ * F

    # 8. Update consciousness
    C += f_consciousness(I, W, M, B[t])
    C *= E

    # 9. Update watchfulness
    W = g_watchfulness(C)

    # 10. Compute alignment projection
    L = projection(C, M)

    # 11. Compute accountability
    Q = np.sum(np.abs(F))

    # 12. Update purpose
    P = compute_tangent(B[t], R[t])

    # Optional: print state
    print(f"Step {t}: C={C}, W={W:.3f}, M={M}, B={B[t]}, R={R[t]}, L={L:.3f}, P={P}, A={A}")
