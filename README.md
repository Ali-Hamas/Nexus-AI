# NEXUS: Governed Cognitive Infrastructure

![NEXUS Version](https://img.shields.io/badge/version-1.0.0-emerald.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**NEXUS** is not an "AI Wrapper." It is an institutional operating system that bridges the gap between chaotic real-world event streams and deterministic strategic execution. It consumes unstructured market events and reduces them into bounded, replayable, and governed cognitive projections.

By wrapping sovereign AI inference in a strict shell of deterministic evidence, verifiable graphs, and Role-Based Access Control (RBAC), NEXUS prevents the operational entropy typical of probabilistic LLM generation. 

*NEXUS does not predict the future. It simulates bounded strategic trajectories constrained by replayable evidence.*

---

## 🏗️ Architecture Philosophy

Most AI applications fail in production because they grant probabilistic systems uncontrolled mutation access to live infrastructure. NEXUS reverses this dynamic.

### 1. Deterministic Extraction
The LLM is bypassed for structured data. A strict JSON-schema pipeline enforces evidence extraction, ensuring that unstructured HTML payloads are converted into deterministic state without latent-space hallucinations.

### 2. Strategic Memory Graph
Knowledge is anchored structurally in a localized SQLite graph, bypassing context-window amnesia and enabling perfectly deterministic replayability. You cannot replay a vector embedding; you *can* replay a graph.

### 3. Institutional Governance
The system constantly monitors convergence anomalies and evidence-poor briefs. If saturation or contradictions occur, NEXUS immediately enters a `GOVERNANCE_FROZEN` state. It intentionally halts mutation to preserve institutional truth.

### 4. Bounded Simulation
Counterfactual strategic projections (e.g., "What if a competitor drops pricing by 15%?") are cleanly sandboxed. The simulation evaluates structural boundaries and mathematically decays confidence the further out the temporal horizon stretches. 

### 5. Graceful Degradation
If the sovereign inference engine (Local LLaMA) crashes, the Event Router catches the exception, updates the platform state to `DEGRADED`, and falls back to deterministic regex extraction. The mesh survives the loss of its smartest components.

---

## 🚀 Quick Start

### Prerequisites
- Node.js 20+
- Python 3.11+
- SQLite3

### Boot Sequence

You can launch the entire stack (Backend, Frontend, and Watcher services) using the unified boot script:

```powershell
# Windows
.\launch_nexus.ps1
```

If you need to boot the subsystems individually for debugging:

**Backend (FastAPI)**
```bash
cd nexus-backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements-lock.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Frontend (Next.js 14)**
```bash
cd nexus-frontend
npm install
npm run dev
```

---

## 🛡️ Role-Based Access Control (RBAC)

NEXUS implements **Cognitive Viewports**. Roles do not just gate API endpoints; they gate situational awareness to prevent executive overload.

- `SYSTEM_ADMIN`: Full access to the raw topology, heartbeat pulses, and chaotic event feeds.
- `EXECUTIVE`: Experiences a sparse, muted strategic dashboard. Noise is constitutionally hidden.
- `ANALYST`: Can simulate bounded scenarios but cannot bypass governance approval.

---

## 💥 Chaos Engineering

NEXUS is designed to survive infrastructure failure. To test the system's resilience, you can inject chaos into the mesh via the Operations Command Center:

- **Queue Saturation**: Floods the governance queue to trigger a `GOVERNANCE_FROZEN` state, proving the system will block speculative simulations to protect data integrity.
- **Inference Timeout**: Forces the sovereign model offline to demonstrate the graceful fallback to the Deterministic Regex Extractor.

---

## 📂 Project Structure

```text
NEXUS-AI/
├── nexus-backend/               # Python/FastAPI Infrastructure
│   ├── app/
│   │   ├── api/                 # Endpoint routers (Simulation, Orchestrator, Auth)
│   │   ├── auth/                # RBAC and Viewport Governance
│   │   ├── chaos/               # Distributed Failure Injectors
│   │   ├── db/                  # SQLite Models & Engine
│   │   ├── events/              # Event Bus & Governance Queue
│   │   ├── services/            # Inference Routers & Watcher Mesh
│   │   └── simulation/          # Bounded Scenario Engine
│   └── tests/                   # Verification and Audit Scripts
│
├── nexus-frontend/              # Next.js 14 Dashboard
│   ├── app/                     # App Router, Layouts, and UI
│   ├── components/              # Topology Graphs and Integrity Panels
│   └── public/                  # Static Assets
│
├── launch_nexus.ps1             # Unified Boot Script
├── launch_nexus_minimal.ps1     # Nuclear Offline Survivability Boot
└── emergency_recovery.md        # Demo Continuation Doctrine
```

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
