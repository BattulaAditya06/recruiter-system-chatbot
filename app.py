"""
app.py

Main entry point.
"""

from rag.loader import load_job_description
from graph.builder import graph
from nodes.final_report import print_report


def main():

    print("=" * 80)
    print("HirePilot AI")
    print("AI Recruitment Assistant")
    print("=" * 80)

    jd = load_job_description(
        "ai_engineer.txt"
    )

    state = {

        "job_description": jd,

        "parsed_job": None,

        "rewritten_job": None,

        "retrieved_candidates": [],

        "screened_candidates": [],

        "interview_questions": [],

        "final_report": None

    }

    result = graph.invoke(state)

    print()

    print("=" * 80)
    print("REWRITTEN JOB DESCRIPTION")
    print("=" * 80)

    print(result["rewritten_job"])

    print()

    print_report(
        result["final_report"]
    )


if __name__ == "__main__":
    main()