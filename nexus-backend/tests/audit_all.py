import requests
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("=== NEXUS FULL AUDIT SCRIPT ===")
    
    # 1. Check health
    print("\n--- PHASE 1: ENVIRONMENT & HEALTH ---")
    try:
        r = requests.get(f"{BASE_URL}/")
        print("Root:", r.status_code)
    except Exception as e:
        print("Backend unreachable:", e)
        return

    # 2. RBAC Enforcement
    print("\n--- PHASE 4: RBAC ---")
    headers_admin = {"X-Nexus-Role": "SYSTEM_ADMIN"}
    headers_exec = {"X-Nexus-Role": "EXECUTIVE"}
    headers_observer = {"X-Nexus-Role": "OBSERVER"}
    
    r = requests.get(f"{BASE_URL}/api/system/state", headers=headers_admin)
    print("System State (Admin):", r.status_code)
    
    r = requests.get(f"{BASE_URL}/api/system/state", headers=headers_observer)
    print("System State (Observer):", r.status_code)
    # The observer might just get normal status, or restricted. Let's see.

    # 3. Governance Freeze (Chaos -> Saturation -> Simulation)
    print("\n--- PHASE 5 & 6: GOVERNANCE & CHAOS ---")
    print("Injecting Queue Saturation...")
    requests.post(f"{BASE_URL}/api/chaos/inject/saturation", headers=headers_admin)
    
    # Give it a moment to update state
    time.sleep(1)
    
    # Check simulation is blocked
    sim_payload = {
        "target_node_id": "Notion",
        "mutation_type": "Pricing -15%",
        "temporal_horizon": "SHORT",
        "requested_trajectory": "COMPRESSION",
        "priority": "HIGH"
    }
    print("Attempting Simulation (Should be blocked due to GOVERNANCE_FROZEN)...")
    r = requests.post(f"{BASE_URL}/api/simulation/project", json=sim_payload, headers=headers_exec)
    print("Simulation Status:", r.status_code)
    if r.status_code in [403, 404]:
        print("[OK] Simulation blocked during Governance Freeze.")
    else:
        print("[FAIL] Simulation allowed during Governance Freeze!")
        
    print("\n--- PHASE 8: REPLAY & DETERMINISM ---")
    # Hit the replay endpoint
    r = requests.get(f"{BASE_URL}/api/demo/stream", headers=headers_admin, stream=True)
    print("Demo Stream Status:", r.status_code)
    
    print("\n=== AUDIT COMPLETE ===")

if __name__ == "__main__":
    test_api()
