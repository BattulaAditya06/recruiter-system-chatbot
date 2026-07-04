"""
final_report.py
"""

from schemas.report_schema import (
    CandidateReport,
    FinalReport
)


def generate_final_report(
        jd,
        screened_candidates
):

    reports = []

    shortlisted = 0
    hold = 0
    rejected = 0

    for candidate in screened_candidates:

        if candidate["decision"] == "SHORTLIST":
            shortlisted += 1

        elif candidate["decision"] == "HOLD":
            hold += 1

        else:
            rejected += 1

        reports.append(

            CandidateReport(

                candidate_name=candidate["candidate_name"],

                decision=candidate["decision"],

                overall_score=candidate["overall_score"],

                mandatory_match=candidate["mandatory_match"],

                strengths=candidate["strengths"],

                weaknesses=candidate["weaknesses"],

                interview_focus=candidate["interview_focus"],

                reasoning=candidate["reasoning"]

            )

        )

    return FinalReport(

        job_title=jd.job_title,

        candidates_screened=len(screened_candidates),

        shortlisted=shortlisted,

        hold=hold,

        rejected=rejected,

        reports=reports

    )
if __name__ == "__main__":

        from rag.loader import load_job_description
        from nodes.parse_jd import parse_job_description
        from rag.retriever import retrieve_candidate_evidence
        from nodes.screen_candidates import screen_candidate

        jd_text = load_job_description("ai_engineer.txt")

        jd = parse_job_description(jd_text)

        candidates = retrieve_candidate_evidence(jd.description)

        screened = []

        for candidate in candidates:

            screened.append(
                screen_candidate(
                    jd,
                    candidate
                )
            )

        report = generate_final_report(
            jd,
            screened
        )

        print(report.model_dump_json(indent=4))