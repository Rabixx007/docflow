from planner.planner import plan_and_validate
from parser.parser import DocTree

tree = DocTree("samples/sample.docx")
bp = tree.blueprint()
ops = plan_and_validate("Make the first heading Heading 1 style", bp)
print(ops)