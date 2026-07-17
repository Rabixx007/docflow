from docx import Document
from schema.operations import SetStyle, FindReplace, InsertTOC, SetFooterPageNumbers, BoldSpan


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
        elif isinstance(op, SetFooterPageNumbers):
            self._set_footer_page_numbers(op)
        elif isinstance(op, BoldSpan):
            self._bold_span(op)
        else:
            raise ValueError(f"Unknown operation type: {type(op)}")
        
    def _set_style(self, op: SetStyle):
        para = self.tree.blocks[op.block_id]
        para.style = op.target_style