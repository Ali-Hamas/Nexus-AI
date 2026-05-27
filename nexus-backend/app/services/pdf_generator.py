import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from typing import Dict, Any

# =========================================================================
# NEXUS - PDF GENERATION LAYER
# =========================================================================

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")

def generate_executive_brief(competitor: str, diff_data: Dict[str, Any], telemetry: Dict[str, Any], governance: Dict[str, Any]) -> str:
    """
    Generates a deterministic PDF executive intelligence brief.
    Returns the file path of the generated PDF.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    filename = f"NEXUS_Brief_{competitor}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    story.append(Paragraph(f"NEXUS Executive Intelligence Brief: {competitor}", styles['Title']))
    story.append(Spacer(1, 12))
    
    # Governance Metadata
    story.append(Paragraph("<b>Governance Approval Metadata</b>", styles['Heading2']))
    story.append(Paragraph(f"Approved By: {governance.get('reviewer', 'System')}", styles['Normal']))
    story.append(Paragraph(f"Action: {governance.get('action', 'N/A')}", styles['Normal']))
    story.append(Paragraph(f"Notes: {governance.get('notes', 'None')}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Dual Scoring
    story.append(Paragraph("<b>Intelligence Scoring</b>", styles['Heading2']))
    story.append(Paragraph(f"Impact Score: {diff_data.get('impact_score', 'N/A')}/10", styles['Normal']))
    story.append(Paragraph(f"Reason: {diff_data.get('impact_reason', 'N/A')}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Semantic Diffs Summary
    story.append(Paragraph("<b>Semantic Diff Summary</b>", styles['Heading2']))
    additions = diff_data.get('additions', {})
    removals = diff_data.get('removals', {})
    
    story.append(Paragraph(f"Additions Detected: {len(additions.keys())}", styles['Normal']))
    story.append(Paragraph(f"Removals Detected: {len(removals.keys())}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Telemetry
    story.append(Paragraph("<b>Infrastructure Telemetry</b>", styles['Heading2']))
    story.append(Paragraph(f"Tokens Saved: {telemetry.get('tokens_saved', 0)}", styles['Normal']))
    story.append(Paragraph(f"Inference Bypassed: {telemetry.get('inference_bypassed', False)}", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    
    return filepath
