from pocketflow import Flow
# Import all node classes from nodes.py
from app.nodes import (
    IdentifyAbstractions,
    AnalyzeRelationships,
    OrderChapters,
    WriteChapters,
    CombineTutorial
)

def create_tutorial_flow():
    """Creates and returns the codebase tutorial generation flow."""

    # Instantiate nodes

    identify_abstractions = IdentifyAbstractions(max_retries=5, wait=20)
    # analyze_relationships = AnalyzeRelationships(max_retries=5, wait=20)
    # order_chapters = OrderChapters(max_retries=5, wait=20)
    # write_chapters = WriteChapters(max_retries=5, wait=20) # This is a BatchNode
    # combine_tutorial = CombineTutorial()

    # # Connect nodes in sequence based on the design
    # fetch_documents >> identify_abstractions
    # identify_abstractions >> analyze_relationships
    # analyze_relationships >> order_chapters
    # order_chapters >> write_chapters
    # write_chapters >> combine_tutorial

    # Create the flow starting with FetchRepo
    tutorial_flow = Flow(start=identify_abstractions)

    return tutorial_flow