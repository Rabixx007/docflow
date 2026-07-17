from pydantic import BaseModel
from typing import Literal


class SetStyle(BaseModel):
    op: Literal["set_style"]
    block_id: str
    target_style: str
    
class FindReplace(BaseModel):
    op: Literal["find_replace"]
    block_id: str
    find: str
    replace: str
    
from typing import Union, Annotated
from pydantic import Field

class InsertTOC(BaseModel):
    op: Literal["insert_toc"]
    after_block_id: str


class SetFooterPageNumbers(BaseModel):
    op: Literal["set_footer_page_numbers"]
    enabled: bool


class BoldSpan(BaseModel):
    op: Literal["bold_span"]
    block_id: str
    start: int
    end: int
    
Operation = Annotated[Union[SetStyle, FindReplace, InsertTOC, SetFooterPageNumbers, BoldSpan], Field(discriminator="op")]

class OperationList(BaseModel):
    operations: list[Operation]
    
if __name__ == "__main__":
    data = {
        "operations": [
            {"op": "set_style", "block_id": "p001", "target_style": "Heading 2"},
            {"op": "find_replace", "block_id": "p003", "find": "foo", "replace": "bar"},
            {"op": "insert_toc", "after_block_id": "p000"},
            {"op": "set_footer_page_numbers", "enabled": True},
            {"op": "bold_span", "block_id": "p003", "start": 0, "end": 5},
        ]
    }
    parsed = OperationList(**data)
    for o in parsed.operations:
        print(o)