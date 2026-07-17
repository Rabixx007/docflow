from docx import Document
from docx.text.paragraph import Paragraph
from collections import defaultdict
import json


class DocTree:
    def __init__(self, path: str):
        self.doc = Document(path)
        self.blocks: dict[str, Paragraph] = {}
        self.style_index: dict[str, list[str]] = defaultdict(list)
        self.order: list[str] = []
        self._build()

    def _build(self):
        for i, para in enumerate(self.doc.paragraphs):

            block_id = f"p{i:03d}"
            self.blocks[block_id] = para
            self.order.append(block_id)

            style_name = para.style.name if para.style else "Normal"
            self.style_index[style_name].append(block_id)
    
    def heading_level(self, para: Paragraph) -> int | None:
        name = para.style.name if para.style else ""
        if name.startswith("Heading "):
            try:
                return int(name.split(" ")[-1])
            except ValueError:
                return None
        return None
    
    def blueprint(self) -> list[dict]:
        out = []
        i = 0
        while i < len(self.order):
            block_id = self.order[i]
            para = self.blocks[block_id]
            length = sum(len(run.text) for run in para.runs)

            if length == 0:
                # collapse a run of consecutive empty paragraphs into one entry
                start = i
                while i < len(self.order) and sum(len(r.text) for r in self.blocks[self.order[i]].runs) == 0:
                    i += 1
                end = i - 1
                out.append({
                    "id_range": f"{self.order[start]}:{self.order[end]}",
                    "style": "Normal",
                    "count": end - start + 1,
                    "note": "blank paragraph spacing",
                })
                continue

            out.append({
                "id": block_id,
                "style": para.style.name if para.style else "Normal",
                "length": length,
                "heading_level": self.heading_level(para),
                "font": para.runs[0].font.name if para.runs else None,
            })
            i += 1
        return out


if __name__ == "__main__":
    tree = DocTree("../samples/sample.docx")
    print(json.dumps(tree.blueprint(), indent=2))
