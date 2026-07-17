# planner/planner.py
from google import genai
from dotenv import load_dotenv
from schema.operations import OperationList
from pydantic import ValidationError
import json
import os

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

PLANNER_SYSTEM_PROMPT = """You are a document-editing planner. You receive:
1. A natural-language instruction from the user.
2. A blueprint: a JSON list of paragraph objects, each with id, style,
   length, heading_level, and font. You have NO access to the actual text.

Your job is to output a JSON object of this exact shape:
{"operations": [ ... ]}

Each item in "operations" must be one of:
- {"op": "set_style", "block_id": "<id>", "target_style": "<style name>"}
- {"op": "find_replace", "block_id": "<id>", "find": "<text>", "replace": "<text>"}
- {"op": "insert_toc", "after_block_id": "<id>"}
- {"op": "bold_span", "block_id": "<id>", "start": <int>, "end": <int>}

Respond with ONLY that JSON object. No prose, no markdown fences, no preamble.
Reference blocks only by ids that appear in the blueprint — never invent one."""


def _call_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config={
            "system_instruction": PLANNER_SYSTEM_PROMPT,
            "response_mime_type": "application/json",
        },
    )
    return response.text


def plan(instruction: str, blueprint: list[dict]) -> str:
    prompt = f"Instruction: {instruction}\n\nBlueprint:\n{json.dumps(blueprint)}"
    return _call_gemini(prompt)


def plan_and_validate(instruction: str, blueprint: list[dict]) -> list:
    raw = plan(instruction, blueprint)
    try:
        return OperationList.model_validate_json(raw).operations
    except ValidationError as e:
        retry_prompt = (
            f"Instruction: {instruction}\n\nBlueprint:\n{json.dumps(blueprint)}\n\n"
            f"Your previous response failed validation with this error:\n{e}\n"
            f"Fix it and respond with ONLY the corrected JSON object."
        )
        raw2 = _call_gemini(retry_prompt)
        try:
            return OperationList.model_validate_json(raw2).operations
        except ValidationError as e2:
            raise ValueError(f"Planner failed validation twice: {e2}") from e2