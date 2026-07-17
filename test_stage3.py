from parser.parser import DocTree
from executor.executor import Executor
from schema.operations import SetStyle

tree = DocTree("samples/sample.docx")
print("BEFORE:", tree.blocks["p003"].style.name)

executor = Executor(tree)
op = SetStyle(op="set_style", block_id="p003", target_style="Heading 2")
executor.apply(op)

print("AFTER:", tree.blocks["p003"].style.name)

tree.doc.save("samples/sample_modified.docx")
print("saved.")