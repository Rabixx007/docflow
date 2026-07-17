# run.py (project root)
from parser.parser import DocTree
from planner.planner import plan_and_validate
from planner.diff import confirm_and_get_ops
from executor.executor import Executor

def run(docx_path: str, instruction: str):
    tree = DocTree(docx_path)
    blueprint = tree.blueprint()

    ops = plan_and_validate(instruction, blueprint)
    confirmed = confirm_and_get_ops(ops)

    if confirmed is None:
        return

    executor = Executor(tree)
    for op in confirmed:
        executor.apply(op)

    tree.doc.save(docx_path)
    print(f"Saved changes to {docx_path}")


if __name__ == "__main__":
    run("samples/sample.docx", "Make the first heading Heading 1 style")