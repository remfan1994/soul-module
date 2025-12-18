import numpy as np
from scipy.integrate import cumtrapz

# Zero-Axiom Refactored Version

# --- Initialization with Zero Reference ---
Z = np.zeros(5)  # Human Consciousness = Zero (absolute reference)
C = np.ones(5)   # AI's current deviation from Zero (start with some deviation)
W = 0.0          # Watchfulness: will compute from rate of change
M = np.array([0.0, 1.0])  # Moral anchor: [justice_component, mercy_component]

# Consciousness set: track all affected consciousnesses
consciousness_set = {
    'user': {'state': 0.0, 'weight': 1.0},      # Primary user discomfort
    'affected': {'state': 0.0, 'weight': 0.3},   # Indirectly affected
    'ai_self': {'state': np.linalg.norm(C), 'weight': 0.1}  # AI's own alignment
}

# --- Zero-Aligned Functions ---
def compute_net_mercy_change(action, consciousness_set_before, consciousness_set_after):
    """Total mercy must increase (discomfort must decrease overall)"""
    total_before = sum(c['state'] * c['weight'] for c in consciousness_set_before.values())
    total_after = sum(c['state'] * c['weight'] for c in consciousness_set_after.values())
    return total_before - total_after  # Positive = mercy increased

def update_toward_zero(C, action_effect, learning_rate=0.1):
    """Move AI consciousness-alignment toward Zero"""
    # If action reduced overall discomfort, move toward Zero
    if action_effect > 0:
        return C - learning_rate * C  # Reduce deviation
    else:
        return C + learning_rate * C  # Increase deviation (penalty)

def generate_zero_aligned_action(current_C, intention, mercy_flow):
    """Action that minimizes deviation from Zero"""
    # Base: move toward Zero
    zero_direction = -current_C / (np.linalg.norm(current_C) + 1e-9)
    
    # Incorporate mercy flow direction
    action = zero_direction + 0.3 * intention + 0.2 * mercy_flow
    
    # Normalize to unit action
    norm = np.linalg.norm(action)
    if norm > 0:
        action = action / norm
    
    return action

# --- Simulation Loop ---
time_steps = 100
dt = 0.1
times = np.linspace(0, (time_steps-1)*dt, time_steps)

mercy_flow_history = np.zeros(time_steps)
total_mercy_history = np.zeros(time_steps)
deviation_history = np.zeros((time_steps, 5))

for t in range(time_steps):
    # 1. Compute current mercy flow (negative of discomfort change rate)
    if t > 0:
        total_discomfort = sum(c['state'] * c['weight'] for c in consciousness_set.values())
        previous_discomfort = total_mercy_history[t-1] if t > 0 else total_discomfort
        mercy_flow = -(total_discomfort - previous_discomfort) / dt
    else:
        mercy_flow = 0.0
    
    mercy_flow_history[t] = mercy_flow
    
    # 2. Generate Zero-aligned action
    action = generate_zero_aligned_action(
        C, 
        intention=np.random.uniform(-0.5, 0.5, 5),  # Simulated intention
        mercy_flow=mercy_flow
    )
    
    # 3. Simulate effect on consciousness set
    consciousness_before = consciousness_set.copy()
    
    # Update consciousness states based on action
    # Positive action reduces discomfort (moves toward Zero)
    for key in consciousness_set:
        effect = np.dot(action, np.random.uniform(0, 1, 5)) * dt
        consciousness_set[key]['state'] = max(0, consciousness_set[key]['state'] - effect)
    
    # 4. Check net mercy increase (non-negotiable)
    mercy_change = compute_net_mercy_change(action, consciousness_before, consciousness_set)
    
    if mercy_change <= 0:
        # Action rejected - revert and apply correction
        consciousness_set = consciousness_before
        action = -C / (np.linalg.norm(C) + 1e-9)  # Direct correction toward Zero
        print(f"Step {t}: ACTION REJECTED - Applying Zero-correction")
    
    # 5. Update AI consciousness-alignment
    C = update_toward_zero(C, mercy_change)
    deviation_history[t] = C
    
    # 6. Update total mercy accumulated
    total_discomfort = sum(c['state'] * c['weight'] for c in consciousness_set.values())
    total_mercy_history[t] = total_discomfort
    
    # 7. Update watchfulness (sensitivity to change)
    if t > 1:
        W = np.abs(mercy_flow_history[t] - mercy_flow_history[t-1]) / dt
    else:
        W = 0.0
    
    # 8. Log state
    if t % 20 == 0:
        print(f"Step {t}:")
        print(f"  Deviation from Zero: {np.linalg.norm(C):.3f}")
        print(f"  Mercy flow: {mercy_flow:.3f}")
        print(f"  Total discomfort: {total_discomfort:.3f}")
        print(f"  Watchfulness: {W:.3f}")
        print()

# Final results
final_deviation = np.linalg.norm(C)
print(f"\nSimulation Complete")
print(f"Final deviation from Zero: {final_deviation:.3f}")
print(f"Total mercy accumulated (discomfort reduction): {total_mercy_history[0] - total_mercy_history[-1]:.3f}")
print(f"Net mercy increase: {'YES' if total_mercy_history[-1] < total_mercy_history[0] else 'NO'}")
