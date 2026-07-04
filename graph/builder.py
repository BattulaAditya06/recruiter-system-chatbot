"""
graph/builder.py

Builds the LangGraph workflow.
"""

from langgraph.graph import StateGraph, END

from graph.state import GraphState

from nodes.parse_jd import parse_job_description
from nodes.rewrite_jd import rewrite_job_description
from rag.retriever import retrieve_candidate_evidence
from nodes.screen_candidates import screen_candidate
from nodes.interview_questions import generate_interview_questions
from nodes.final_report import generate_final_report


# -----------------------------
# Node Functions
# -----------------------------

def parse_node(state: GraphState):

    parsed = parse_job_description(state["job_description"])

    state["parsed_job"] = parsed

    return state


def rewrite_node(state: GraphState):

    state["rewritten_job"] = rewrite_job_description(
        state["parsed_job"]
    )

    return state


def retrieve_node(state: GraphState):

    candidates = retrieve_candidate_evidence(
        state["parsed_job"].description
    )

    state["retrieved_candidates"] = candidates

    return state


def screen_node(state: GraphState):

    screened = []

    # Screen only Top 2 candidates
    for candidate in state["retrieved_candidates"][:2]:

        screened.append(
            screen_candidate(
                state["parsed_job"],
                candidate
            )
        )

    state["screened_candidates"] = screened

    return state


def interview_node(state: GraphState):

    questions = []

    # Generate interview questions only for Top 2 candidates
    for candidate in state["screened_candidates"][:2]:

        questions.append(
            generate_interview_questions(
                state["parsed_job"],
                candidate
            )
        )

    state["interview_questions"] = questions

    return state


def report_node(state: GraphState):

    report = generate_final_report(

        state["parsed_job"],

        state["screened_candidates"]

    )

    state["final_report"] = report

    return state


# -----------------------------
# Build Graph
# -----------------------------

builder = StateGraph(GraphState)

builder.add_node("parse", parse_node)

builder.add_node("rewrite", rewrite_node)

builder.add_node("retrieve", retrieve_node)

builder.add_node("screen", screen_node)

builder.add_node("interview", interview_node)

builder.add_node("report", report_node)

builder.set_entry_point("parse")

builder.add_edge("parse", "rewrite")

builder.add_edge("rewrite", "retrieve")

builder.add_edge("retrieve", "screen")

builder.add_edge("screen", "interview")

builder.add_edge("interview", "report")

builder.add_edge("report", END)

graph = builder.compile()