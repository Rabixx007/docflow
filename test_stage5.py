# test_stage5.py
from planner.planner import plan_and_validate
from planner.diff import confirm_and_get_ops
from parser.parser import DocTree

tree = DocTree("samples/sample.docx")
bp = tree.blueprint()
ops = plan_and_validate("Make the first heading Heading 1 style", bp)

result = confirm_and_get_ops(ops)
if result:
    print("Confirmed, would now execute:", result)
else:
    print("Nothing to execute.")