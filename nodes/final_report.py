"""
final_report.py

Generates the final recruitment report.
"""

from schemas.report_schema import CandidateReport, FinalReport


def generate_final_report(jd, screened_candidates):

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

                matched=candidate["matched"],

                missing=candidate["missing"],

                preferred=candidate["preferred"],

                strengths=candidate["strengths"],

                weaknesses=candidate["weaknesses"],

                improvements=candidate["improvements"],

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


def print_report(report: FinalReport):

    print("\n" + "=" * 80)
    print("FINAL RECRUITMENT REPORT")
    print("=" * 80)

    print(f"Job Title           : {report.job_title}")
    print(f"Candidates Screened : {report.candidates_screened}")
    print(f"Shortlisted         : {report.shortlisted}")
    print(f"Hold                : {report.hold}")
    print(f"Rejected            : {report.rejected}")

    print("=" * 80)

    for candidate in report.reports:

        print(f"\nCandidate : {candidate.candidate_name}")
        print("-" * 80)

        print(f"Decision          : {candidate.decision}")
        print(f"Overall Score     : {candidate.overall_score}")
        print(f"Mandatory Match   : {candidate.mandatory_match}%")

        print("\nMatched Skills")
        for skill in candidate.matched:
            print(f"  ✓ {skill}")

        print("\nMissing Skills")
        if candidate.missing:
            for skill in candidate.missing:
                print(f"  ✗ {skill}")
        else:
            print("  None")

        print("\nStrengths")
        for item in candidate.strengths:
            print(f"  ✓ {item}")

        print("\nWeaknesses")
        for item in candidate.weaknesses:
            print(f"  ✗ {item}")

        print("\nImprovement Suggestions")
        for item in candidate.improvements:
            print(f"  • {item}")

        print("\nInterview Focus")
        if candidate.interview_focus:
            for item in candidate.interview_focus:
                print(f"  • {item}")
        else:
            print("  None")

        print("\nReasoning")
        print(candidate.reasoning)

        print("\n" + "=" * 80)


def save_report(report, filename="Recruitment_Report.txt"):

    with open(filename, "w", encoding="utf-8") as f:

        f.write("=" * 80 + "\n")

        f.write("HirePilot AI Recruitment Report\n")

        f.write("=" * 80 + "\n\n")

        f.write(f"Job Title : {report.job_title}\n")

        f.write(f"Candidates Screened : {report.candidates_screened}\n")

        f.write(f"Shortlisted : {report.shortlisted}\n")

        f.write(f"Hold : {report.hold}\n")

        f.write(f"Rejected : {report.rejected}\n\n")

        for candidate in report.reports:

            f.write("-" * 80 + "\n")

            f.write(f"Candidate : {candidate.candidate_name}\n")

            f.write(f"Decision : {candidate.decision}\n")

            f.write(f"Overall Score : {candidate.overall_score}\n")

            f.write(f"Mandatory Match : {candidate.mandatory_match}%\n\n")

            f.write("Strengths\n")

            for item in candidate.strengths:
                f.write(f"  ✓ {item}\n")

            f.write("\nWeaknesses\n")

            for item in candidate.weaknesses:
                f.write(f"  ✗ {item}\n")

            f.write("\nInterview Focus\n")

            for item in candidate.interview_focus:
                f.write(f"  • {item}\n")

            f.write("\nReasoning\n")

            f.write(candidate.reasoning)

            f.write("\n\n")

    print(f"\nReport saved as {filename}")

if __name__ == "__main__":

    from rag.loader import load_job_description
    from nodes.parse_jd import parse_job_description
    from rag.retriever import retrieve_candidate_evidence
    from nodes.screen_candidates import screen_candidate

    jd_text = load_job_description("ai_engineer.txt")

    jd = parse_job_description(jd_text)

    retrieved = retrieve_candidate_evidence(jd.description)

    screened = []

    for candidate in retrieved:

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

    print_report(report)