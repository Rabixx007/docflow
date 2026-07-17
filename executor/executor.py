from docx import Document
from schema.operations import SetStyle, FindReplace, InsertTOC, BoldSpan


class Executor:
    def __init__(self, tree):
        self.tree = tree
        
    def apply(self, op):
        if isinstance(op, SetStyle):
            self._set_style(op)
        elif isinstance(op, FindReplace):
            self._find_replace(op)
        elif isinstance(op, InsertTOC):
            self._insert_toc(op)
        elif isinstance(op, BoldSpan):
            self._bold_span(op)
        else:
            raise ValueError(f"Unknown operation type: {type(op)}")
        
    def _set_style(self, op: SetStyle):
        para = self.tree.blocks[op.block_id]
        para.style = op.target_style
        
    def _find_replace(self, op: FindReplace):
        para = self.tree.blocks[op.block_id]
        for run in para.runs:
            if op.find in run.text:
                run.text = run.text.replace(op.find, op.replace)
                
    def _insert_toc(self, op: InsertTOC):
        para = self.tree.blocks[op.after_block_id]
        new_para = para.insert_paragraph_before("Table of Contents (placeholder)")
        new_para.style = self.tree.doc.styles["Heading 1"]

    def _bold_span(self, op: BoldSpan):
        para = self.tree.blocks[op.block_id]
        full_text = "".join(run.text for run in para.runs)
        target = full_text[op.start:op.end]
        for run in para.runs:
            run.text = ""
        para.runs[0].text = full_text[:op.start]
        b = para.add_run(target)
        b.bold = True
        para.add_run(full_text[op.end:])