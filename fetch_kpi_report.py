import json
from datetime import datetime

def generate_mock_kpi_report():
    """
    Produces a placeholder KPI snapshot that mirrors the structure we need
    for the “domination across all aspects” assessment.
    """
    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "market_share": {
            "overall": 42.7,                # percent of total market
            "segment_breakdown": {
                "consumer": 38.2,
                "enterprise": 47.5,
                "government": 52.1
            },
            "competitor_comparison": {
                "AlphaTech": 39.4,
                "BetaSolutions": 35.8,
                "GammaCorp": 28.1
            }
        },
        "net_promoter_score": {
            "overall_nps": 71,
            "by_product_line": {
                "core_platform": 78,
                "analytics_suite": 68,
                "mobile_app": 64
            }
        },
        "innovation_pipeline": {
            "ideas_submitted_last_quarter": 124,
            "prototypes_completed": 57,
            "features_released": 23,
            "average_cycle_days": 46
        },
        "operational_excellence": {
            "on_time_delivery_pct": 96.3,
            "defect_rate_ppm": 12,
            "first_pass_yield_pct": 98.7
        }
    }
    return report

if __name__ == "__main__":
    # Serialize to JSON for easy readability in the response
    print(json.dumps(generate_mock_kpi_report(), indent=4))