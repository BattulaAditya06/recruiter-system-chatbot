"""
approval.py

Recruiter approval node.
"""


def recruiter_approval(candidate_result: dict) -> bool:
    """
    Ask recruiter whether to continue.

    Returns:
        True -> Continue
        False -> Stop
    """

    print("\n" + "=" * 70)
    print("RECRUITER DECISION")
    print("=" * 70)

    print(f"Candidate : {candidate_result['candidate_name']}")
    print(f"Decision  : {candidate_result['decision']}")
    print(f"Score     : {candidate_result['overall_score']}")

    while True:

        choice = input("\nApprove candidate? (yes/no): ").strip().lower()

        if choice in ["yes", "y"]:
            return True

        if choice in ["no", "n"]:
            return False

        print("Enter yes or no.")

    if __name__ == "__main__":

        sample = {

            "candidate_name": "John",

            "decision": "SHORTLIST",

            "overall_score": 90

        }

        approved = recruiter_approval(sample)

        print()

        print("Approved :", approved)