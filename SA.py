import numpy as np
import csv
import json

# Define your cost function (example: Himmelblau function)
# https://en.wikipedia.org/wiki/Himmelblau%27s_function
def cost(x):
    return (x[0] +  x[1]**2 - 7) ** 2 + (x[0]**2 + x[1] -11) ** 2

# Problem dimension (can be any positive integer)
n               = 2

# Initial temperature
T               = 300.0

# Temperature update rate
cooling_rate    = 0.95

# Minimum temperature (stopping criterion)
T_min           = 0.05

# Maximum iterations
max_iter        = 1000

# Initial solution (random point in [0,1]^n)
x               = np.random.rand(n)

# Initial neighborhood step size
delta           = np.random.rand(n)

# History list to store logs: each entry is a dict
history         = []

# Simulated Annealing main loop
for iteration in range(max_iter):
    # Generate a new candidate solution
    r               = delta * np.random.uniform(-1, 1, size=n)
    x_new           = x + r

    # Evaluate cost at current and new positions
    f_current       = cost(x)
    f_new           = cost(x_new)

    # Accept new point if better, or with probability if worse
    accepted        = False
    if f_new < f_current or np.random.rand() < np.exp(-(f_new - f_current) / T):
        x           = x_new
        T           *= cooling_rate  # Cool down only when move accepted
        accepted    = True
        
    
     # Log details for this iteration
    history.append({
        'iteration': iteration,
        'temperature': T,
        'current_cost': f_current,
        'candidate_cost': f_new,
        'accepted': accepted,
        'x': x.copy().tolist(),
        'step': r.copy().tolist()
    })
    
    print(f"Iter {iteration:4d} | T={T:7.4f} | f(x)={f_current:10.6f} | f(new)={f_new:10.6f} "
          f"| {'ACCEPTED' if accepted else 'REJECTED'} | x={x}")
    
    # Check stopping criterion
    if T < T_min:
        break

# Final result
print("Best solution found:", x)
print("Cost at best solution:", cost(x))


# Save to JSON
with open("history.json", "w") as f_json:
    json.dump(history, f_json, indent=2)

# Save to CSV (flatten nested lists)
with open("history.csv", "w", newline="") as f_csv:
    fieldnames = ['iteration', 'temperature', 'current_cost', 'candidate_cost', 'accepted'] + \
                 [f'x_{i}' for i in range(n)] + [f'step_{i}' for i in range(n)]
    writer = csv.DictWriter(f_csv, fieldnames=fieldnames)
    writer.writeheader()

    for h in history:
        flat_entry = {
            'iteration': h['iteration'],
            'temperature': h['temperature'],
            'current_cost': h['current_cost'],
            'candidate_cost': h['candidate_cost'],
            'accepted': h['accepted']
        }
        for i in range(n):
            flat_entry[f'x_{i}'] = h['x'][i]
            flat_entry[f'step_{i}'] = h['step'][i]
        writer.writerow(flat_entry)
