import os
from app.services.pdf_generator import generate_executive_brief
from app.services.mock_data import get_mock_diff, get_mock_governance_payload

def verify_pdf_generation():
    print("--- Verifying PDF Generation Layer ---")
    
    diff_data = get_mock_diff("pricing_change")
    governance = get_mock_governance_payload()
    telemetry = {"tokens_saved": 1500, "inference_bypassed": False}
    
    pdf_path = generate_executive_brief("Notion", diff_data, telemetry, governance)
    
    assert os.path.exists(pdf_path), "PDF file was not created"
    assert os.path.getsize(pdf_path) > 0, "PDF file is empty"
    
    print(f"PDF generated successfully at: {pdf_path}")
    print("PDF Generation Layer: PASS")

if __name__ == "__main__":
    try:
        verify_pdf_generation()
        print("PHASE 7 VERIFICATION PASSED.")
    except AssertionError as e:
        print(f"VERIFICATION FAILED: {e}")
