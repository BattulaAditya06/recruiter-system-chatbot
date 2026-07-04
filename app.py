"""
HirePilot AI

Main Entry Point
"""
import time
from rag.loader import load_job_description

from graph.builder import graph
from nodes.interview_questions import save_questions
from nodes.final_report import print_report
from nodes.rewrite_jd import save_rewritten_jd
from nodes.final_report import save_report

def main():

    print("=" * 80)
    print("HirePilot AI")
    print("AI Powered Recruitment Assistant")
    print("=" * 80)

    print()

    print("\n[1/6] Loading Job Description...")

    jd_text = load_job_description("ai_engineer.txt")

    print("✓ Job Description Loaded")

    print()

    state = {

        "job_description": jd_text,

        "parsed_job": None,

        "rewritten_job": None,

        "retrieved_candidates": [],

        "screened_candidates": [],

        "interview_questions": [],

        "final_report": None

    }

    print("\n[2/6] Running Recruitment Workflow...")

    workflow_start = time.time()

    result = graph.invoke(state)

    workflow_end = time.time()

    print("✓ Workflow Completed")

    print(
    f"\n✓ Workflow finished in "
    f"{workflow_end - workflow_start:.2f} seconds"
)

    print()

    print("=" * 80)

    print("REWRITTEN JOB DESCRIPTION")

    print("=" * 80)

    print()

    print(result["rewritten_job"])
    save_rewritten_jd(
        result["rewritten_job"]
)

    print()

    print_report(result["final_report"])
    save_questions(
        result["interview_questions"]
)

    save_report(result["final_report"])

    print()

    print("=" * 80)

    print("Workflow Completed Successfully")

    print("=" * 80)


if __name__ == "__main__":

    main()