from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
import uuid
import datetime

class EventMode(str, Enum):
    LIVE = "LIVE"
    REPLAY = "REPLAY"
    CHAOS = "CHAOS"
    SIMULATION = "SIMULATION"

class LifecycleState(str, Enum):
    INGESTED = "INGESTED"
    PARSED = "PARSED"
    CORRELATED = "CORRELATED"
    GRAPHED = "GRAPHED"
    SYNTHESIZED = "SYNTHESIZED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    VERIFIED = "VERIFIED"
    EXECUTIVE_BRIEFED = "EXECUTIVE_BRIEFED"
    ARCHIVED = "ARCHIVED"

class GovernanceState(str, Enum):
    PENDING = "PENDING"
    ESCALATED = "ESCALATED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"

class CanonicalIntelligenceEvent(BaseModel):
    """
    The Institutional Cognition Schema.
    Ensures coherence across graph, governance, synthesis, telemetry, and SSE feeds.
    """
    event_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    correlation_id: Optional[str] = None
    sector: str
    target: str # E.g., Notion, ChatGPT
    
    # Priority & Trust Scoring
    priority_score: float = 0.0
    integrity_score: float = 0.0
    confidence: float = 0.0
    evidence_density: float = 0.0
    lineage_depth: int = 0
    replayability: float = 0.0
    
    # Evidentiary Support
    evidence_anchors: List[str] = Field(default_factory=list)
    source_nodes: List[str] = Field(default_factory=list)
    temporal_support: str = "CURRENT"
    reasoning_scope: str = "LOCAL"
    
    # State & Mode Tracking
    governance_state: str = GovernanceState.PENDING.value
    event_lifecycle_state: str = LifecycleState.INGESTED.value
    event_mode: str = EventMode.LIVE.value
    
    # Payload Context
    action: str # E.g., "DIFFING", "SYNTHESIZED"
    message: str # Human-readable log
    payload: dict = Field(default_factory=dict) # e.g. the diff, the extracted JSON, or the strategic_narrative
    
    # System Epochs & Metadata
    constitution_version: str = "1.0.0"
    schema_epoch: str = "EPOCH_3"
    governance_epoch: str = "EPOCH_3"
    integrity_version: str = "v1"
    timestamp: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")
