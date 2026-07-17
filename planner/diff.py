# planner/diff.py
from schema.operations import SetStyle, FindReplace, InsertTOC, BoldSpan

def _fmt_set_style(op: SetStyle) -> str:
    return f"{op.block_id}: style → {op.target_style}"

def _fmt_find_replace(op: FindReplace) -> str:
    return f"{op.block_id}: replace \"{op.find}\" → \"{op.replace}\""

def _fmt_insert_toc(op: InsertTOC) -> str:
    return f"after {op.after_block_id}: insert Table of Contents"

def _fmt_bold_span(op: BoldSpan) -> str:
    return f"{op.block_id}: bold chars [{op.start}:{op.end}]"

_FORMATTERS = {
    SetStyle: _fmt_set_style,
    FindReplace: _fmt_find_replace,
    InsertTOC: _fmt_insert_toc,
    BoldSpan: _fmt_bold_span,
}

def render_diff(operations: list) -> str:
    lines = [_FORMATTERS[type(op)](op) for op in operations]
    return "\n".join(lines)

# planner/diff.py — add below render_diff()

def confirm_and_get_ops(operations: list) -> list | None:
    print("Planned changes:")
    print(render_diff(operations))
    answer = input("\nApply these changes? [y/N]: ").strip().lower()
    if answer == "y":
        return operations
    print("Aborted — no changes applied.")
    return None