from parser.parser import DocTree
from executor.executor import Executor
from schema.operations import SetStyle, FindReplace, InsertTOC, BoldSpan

tree = DocTree("samples/sample.docx")
executor = Executor(tree)

# test set_style
executor.apply(SetStyle(op="set_style", block_id="p003", target_style="Heading 2"))

# test find_replace
print("BEFORE find_replace:", tree.blocks["p007"].text)
executor.apply(FindReplace(op="find_replace", block_id="p007", find="paperless", replace="digital"))
print("AFTER find_replace:", tree.blocks["p007"].text)

# test insert_toc
executor.apply(InsertTOC(op="insert_toc", after_block_id="p001"))

# test bold_span
print("BEFORE bold_span:", tree.blocks["p011"].text)
executor.apply(BoldSpan(op="bold_span", block_id="p011", start=0, end=4))

tree.doc.save("samples/sample_modified.docx")
print("saved.")