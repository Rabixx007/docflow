# test_stage4_retry.py
from planner.planner import _call_gemini, plan_and_validate
from schema.operations import OperationList
from pydantic import ValidationError
import json
from parser.parser import DocTree

tree = DocTree("samples/sample.docx")
bp = tree.blueprint()

# Monkey-patch plan() temporarily to return something broken on first call
import planner.planner as planner_module

call_count = {"n": 0}
original_call = planner_module._call_gemini

def broken_first_call(prompt):
    call_count["n"] += 1
    if call_count["n"] == 1:
        return '{"operations": [{"op": "set_style", "block_id": "p001"}]}'  # missing target_style
    return original_call(prompt)

planner_module._call_gemini = broken_first_call

ops = plan_and_validate("Make the first heading Heading 1 style", bp)
print("Calls made:", call_count["n"])
print("Result:", ops)