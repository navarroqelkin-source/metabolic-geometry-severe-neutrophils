"""
This script implements a minimal synthetic NET burden model for identifiability demonstration only.
It does not calibrate to patient data, infer disease mechanisms, or validate biological function.
"""

import os
import csv
import numpy as np

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
params_file = os.path.join(script_dir, "parameters_v0.1.tsv")
scenarios_file = os.path.join(script_dir, "scenarios_v0.1.tsv")
outputs_dir = os.path.join(script_dir, "outputs")

def euler_step(B, F, D, C, P, dt):
    # dB/dt = F - [D + C] * B + P
    dBdt = F - (D + C) * B + P
    return B + dBdt * dt

def run_simulation():
    # Load scenarios
    scenarios = []
    with open(scenarios_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            scenarios.append(row)

    t_max = 10.0
    dt = 0.1
    time_points = np.arange(0, t_max + dt, dt)
    
    results = []

    for scen in scenarios:
        s_id = scen["scenario_id"]
        s_name = scen["scenario_name"]
        
        # Parameters
        F = float(scen["F0"])
        D = float(scen["D0"])
        C = float(scen["C0"])
        P = float(scen["P0"])
        KR = float(scen["KR"])
        B_initial = float(scen["B0"])
        
        B_series = [B_initial]
        Y_series = [KR * B_initial]
        
        B_current = B_initial
        for t in time_points[1:]:
            B_next = euler_step(B_current, F, D, C, P, dt)
            B_next = max(0.0, B_next) # Prevent negative burden
            B_series.append(B_next)
            Y_series.append(KR * B_next)
            B_current = B_next
            
        final_B = B_series[-1]
        final_Y = Y_series[-1]
        
        results.append({
            "scenario_id": s_id,
            "scenario_name": s_name,
            "final_B": round(final_B, 3),
            "final_Y": round(final_Y, 3)
        })
        
        if HAS_MATPLOTLIB:
            plt.figure(figsize=(6,4))
            plt.plot(time_points, B_series, label="True Burden (B)")
            plt.plot(time_points, Y_series, label="Observed Biomarker (Y)")
            plt.title(f"Scenario: {s_name}")
            plt.xlabel("Time")
            plt.ylabel("Levels")
            plt.legend()
            plt.savefig(os.path.join(outputs_dir, f"{s_id}_{s_name}.png"))
            plt.close()

    # Save results summary
    output_tsv = os.path.join(outputs_dir, "simulation_results.tsv")
    with open(output_tsv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["scenario_id", "scenario_name", "final_B", "final_Y"], delimiter="\t")
        writer.writeheader()
        writer.writerows(results)

    print("Smoke test completed. Synthetic outputs generated. No biological inference performed.")

if __name__ == "__main__":
    run_simulation()
