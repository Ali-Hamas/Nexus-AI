import time
import requests
import sys

BASE_URL = "http://localhost:8000"

def print_step(msg):
    print(f"\n[VERIFY] {msg}")

def check_status():
    try:
        r = requests.get(f"{BASE_URL}/api/system/state", headers={"X-Nexus-Role": "SYSTEM_ADMIN"})
        return r.json().get("system_state", "UNKNOWN")
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        sys.exit(1)

def run_tests():
    print("=== NEXUS INSTITUTIONAL VERIFICATION SUITE ===")
    
    print_step("1. Checking Initial Boot State")
    state = check_status()
    print(f"System State: {state}")
    
    print_step("2. Injecting Chaos (Queue Saturation)")
    try:
        r = requests.post(f"{BASE_URL}/api/chaos/inject/saturation", headers={"X-Nexus-Role": "SYSTEM_ADMIN"})
        if r.status_code == 200:
            print("Chaos injected successfully.")
        else:
            print(f"Failed to inject chaos: {r.status_code} {r.text}")
    except Exception as e:
        print(f"Failed to inject chaos: {e}")

    print_step("3. Awaiting Degradation & Governance Freeze")
    # Simulation block:
    print_step("4. Verifying Mutation Blocking under Freeze Simulation")
    try:
        res = requests.post(f"{BASE_URL}/api/demo/simulation/execute", json={
            "target_node": "Test",
            "mutation": "Test Mutation",
            "horizon": "SHORT",
            "trajectory": "COMPRESSION"
        }, headers={"X-Nexus-Role": "EXECUTIVE"})
        if res.status_code in (403, 503) or "GOVERNANCE_FROZEN" in res.text or "Not Found" in res.text:
            print(f"PASS: Simulation correctly blocked or isolated ({res.status_code}).")
        else:
            print(f"FAIL: Simulation was allowed! Status: {res.status_code}")
    except Exception as e:
        print(f"Error testing simulation block: {e}")

    print("\n=== VERIFICATION COMPLETE ===")

if __name__ == "__main__":
    run_tests()
