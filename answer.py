import os
import json
from dotenv import load_dotenv
from google import genai
from search import search

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def build_prompt(question, hits):
    context = "\n\n".join(
        f"[{c['case_no']}] {c['text']}"
        for _d, c in hits
    )
        return f"""You are a legal research assistant.
Answer the question using ONLY the passages below.
Cite the case number in square brackets after each claim.
If the passages do not answer the question, say so, set confident to false,
and return an empty list for cases.

PASSAGES:
{context}

QUESTION: {question}"""


SCHEMA = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "cases": {"type": "array", "items": {"type": "string"}},
        "confident": {"type": "boolean"},
    },
    "required": ["answer", "cases", "confident"],
}

DISTANCE_LIMIT = 0.56

REFUSAL = {
    "answer": "I could not find anything in these judgments that covers this.",
    "cases": [],
    "confident": False,
    "passages": [],
}


def ask(question, k=5):
    hits = search(question, k)

    if not hits or hits[0][0] > DISTANCE_LIMIT:
        return REFUSAL

    prompt = build_prompt(question, hits)

    reply = client.interactions.create(
        model="gemini-flash-latest",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": SCHEMA,
        },
    )

    u = reply.usage
    print(u.total_input_tokens, "in,", u.total_output_tokens, "out,",
          u.total_thought_tokens, "thinking,", u.total_tokens, "total")

    out = json.loads(reply.output_text)
    out["passages"] = [{"case_no": c["case_no"], "text": c["text"], "distance": d}
                       for d, c in hits]

    if not out["cases"] or not out["confident"]:   # it read them. it says no.
        return REFUSAL

    return out


if __name__ == "__main__":
    out = ask("the department withheld my retiral dues")
    print(out["answer"])
    print("cases:", out["cases"])