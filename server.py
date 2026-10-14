import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("neodocs")


def load_scans():
    with open(Path(__file__).parent / "scans.json") as f:
        return json.load(f)


@mcp.tool()
def list_test_results(kit_type: str = "") -> list:
    """List the user's saved at-home test scans.

    Use this when the user wants to SEE their scans or asks what a scan showed.
    kit_type is optional: "wellness" or "uti". To see how one value changed
    over time, use get_result_trend instead.
    """
    scans = load_scans()
    if kit_type:
        scans = [s for s in scans if s["kit_type"] == kit_type.lower()]
    return scans


@mcp.tool()
def get_result_trend(parameter: str) -> dict:
    """Show how ONE measured value changed across scans over time.

    Use this when the user asks if something is going up, going down, or
    staying the same. parameter is a name like "protein", "glucose",
    "ketones", "ph", "leukocytes", or "nitrites". To see full scans instead,
    use list_test_results.
    """
    values = []
    for scan in load_scans():
        if parameter.lower() in scan["results"]:
            values.append(
                {"date": scan["scan_date"][:10], "value": scan["results"][parameter.lower()]}
            )
    return {"parameter": parameter, "values": values}

@mcp.tool()
def check_out_of_range_results() -> dict:
    """Check the most recent scan and list any values that are not normal.

    Use this when the user asks if their latest scan looks normal. To learn
    what a value MEANS, use search_health_guidance instead. Not a diagnosis.
    """
    scan = load_scans()[-1]
    flags = []
    for name, value in scan["results"].items():
        if name == "ph":
            if value < 5.0 or value > 8.0:
                flags.append(f"ph: {value}")
        elif value > 0:
            flags.append(f"{name}: level {value}")
    return {"scan_id": scan["scan_id"], "flags": flags,
            "note": "Mock ranges. Not a diagnosis. See a doctor about any concern."}


@mcp.tool()
def search_health_guidance(question: str) -> list:
    """Search a small health knowledge base and return the 2 most relevant sections.

    Use this when the user asks what a value or term MEANS, for example
    "what does nitrite mean". Do not use it to look up the user's own scans.
    """
    path = Path(__file__).parent / "knowledge_base.md"
    chunks = path.read_text(encoding="utf-8").split("\n## ")[1:]
    words = [w.strip("?.,!").lower() for w in question.split() if len(w) > 3]

    scored = []
    for chunk in chunks:
        score = sum(1 for w in words if w in chunk.lower())
        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [chunk for score, chunk in scored[:2]] or ["Nothing relevant found."]


@mcp.resource("neodocs://kits")
def kits() -> str:
    """The test kits and which values each one measures."""
    return json.dumps({
        "wellness": ["glucose", "protein", "ketones", "ph", "leukocytes", "nitrites"],
        "uti": ["ph", "leukocytes", "nitrites"],
    })


@mcp.prompt()
def explain_my_latest_result() -> str:
    """Explain the user's latest scan in simple words."""
    return ("Check my latest scan with check_out_of_range_results, then use "
            "search_health_guidance to explain anything flagged in simple words. "
            "Remind me this is not a diagnosis.")

if __name__ == "__main__":
    mcp.run(transport="stdio")