from pathlib import Path

import tiktoken

from server import search_health_guidance

enc = tiktoken.get_encoding("cl100k_base")

full_text = (Path(__file__).parent / "knowledge_base.md").read_text(encoding="utf-8")
result_text = "\n\n".join(search_health_guidance("what does nitrite mean"))

print("Whole knowledge base:", len(enc.encode(full_text)), "tokens")
print("Search result (2 sections):", len(enc.encode(result_text)), "tokens")