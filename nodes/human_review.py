"""
human_review.py

Human-in-the-loop review node.
"""

def human_review(screened_candidates):

    reviewed = []

    print("\n" + "=" * 80)
    print("HUMAN IN THE LOOP REVIEW")
    print("=" * 80)

    for candidate in screened_candidates:

        print("\nCandidate :", candidate["candidate_name"])

        print("AI Decision :", candidate["decision"])

        print("Overall Score :", candidate["overall_score"])

        print("Mandatory Match :", candidate["mandatory_match"], "%")

        print("\nMatched Skills")

        for s in candidate["matched"]:
            print("✓", s)

        print("\nMissing Skills")

        for s in candidate["missing"]:
            print("✗", s)

        print("\nReason")

        print(candidate["reasoning"])

        print("\nRecruiter Decision")

        print("1. Accept AI Recommendation")

        print("2. SHORTLIST")

        print("3. HOLD")

        print("4. REJECT")

        choice = input("Choice : ").strip()

        final_decision = candidate["decision"]

        override = False

        if choice == "2":
            final_decision = "SHORTLIST"
            override = True

        elif choice == "3":
            final_decision = "HOLD"
            override = True

        elif choice == "4":
            final_decision = "REJECT"
            override = True

        candidate["ai_decision"] = candidate["decision"]

        candidate["decision"] = final_decision

        candidate["human_override"] = override

        reviewed.append(candidate)

    return reviewed