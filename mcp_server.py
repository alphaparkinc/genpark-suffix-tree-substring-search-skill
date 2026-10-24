"""MCP Server for GenPark Suffix Tree Substring Search.
100% Python Standard Library.
"""

import json
import sys
from client import SuffixTree

st = SuffixTree()

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "index_document",
                        "description": "Build suffix tree index for target text corpus",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"text": {"type": "string"}},
                            "required": ["text"]
                        }
                    },
                    {
                        "name": "search_substring",
                        "description": "Locate all starting offsets of a query substring",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"pattern": {"type": "string"}},
                            "required": ["pattern"]
                        }
                    },
                    {
                        "name": "check_substring_exists",
                        "description": "Fast boolean check whether substring exists in corpus",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"pattern": {"type": "string"}},
                            "required": ["pattern"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "index_document":
            doc = args.get("text", "")
            st.build(doc)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": f"Indexed text length {len(doc)} chars."}]}
            }
        elif name == "search_substring":
            p = args.get("pattern", "")
            offsets = st.search(p)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps({"pattern": p, "occurrences": len(offsets), "offsets": offsets}, indent=2)}]}
            }
        elif name == "check_substring_exists":
            p = args.get("pattern", "")
            exists = st.contains(p)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps({"pattern": p, "exists": exists})}]}
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
