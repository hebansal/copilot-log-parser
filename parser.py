import json
import sys
import os

def extract_user_prompt(data):
    """Extracts and formats user input text from a valid data token block."""
    if "k" in data and isinstance(data["k"], list) and "inputText" in data["k"]:
        return f"\n### 👤 User\n> {data.get('v', '')}\n\n"
    return ""

def format_inline_reference(ref):
    """Processes interactive symbol or file system path metadata fragments."""
    if not isinstance(ref, dict):
        return ""
        
    # Case A: Named function/variable symbol reference
    if "name" in ref:
        return f" `{ref['name']}` "
        
    # Case B: Direct file system path reference
    if "fsPath" in ref:
        full_path = ref["fsPath"]
        parts = [p for p in full_path.split('/') if p]
        
        # If the path is deep enough, keep the last two parts (e.g., 'cache/index.js')
        if len(parts) >= 2:
            return f" `{parts[-2]}/{parts[-1]}` "
        return f" `{os.path.basename(full_path)}` "
        
    return ""


def extract_responses(data):
    """Normalizes raw variation arrays down to flat sequential response chunks."""
    if data.get("kind") != 2:
        return []
        
    v_data = data.get("v", [])
    if isinstance(v_data, list):
        return v_data
        
    if isinstance(v_data, dict):
        requests = v_data.get("requests", [])
        if isinstance(requests, list):
            responses = []
            for req in requests:
                if isinstance(req, dict):
                    responses.extend(req.get("response", []))
            return responses
            
    return []

def process_response_item(resp):
    """Transforms individual raw stream items into clear Markdown sections."""
    if not isinstance(resp, dict):
        return ""
        
    if resp.get("kind") == "thinking" and resp.get("value"):
        return f"#### 🧠 Copilot Thoughts\n*{resp['value'].strip()}*\n\n"
        
    if resp.get("value"):
        return resp["value"]
        
    if "inlineReference" in resp:
        return format_inline_reference(resp["inlineReference"])
        
    return ""

def parse_copilot_stream(input_file, output_file):
    """Main streaming file router reading raw streams to output Markdown."""
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        outfile.write("# Parsed Copilot Chat Session\n\n")
        
        for line in infile:
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    continue

                # 1. Parse user queries
                outfile.write(extract_user_prompt(data))
                
                # 2. Extract and parse copilot response blocks
                for resp in extract_responses(data):
                    outfile.write(process_response_item(resp))
                                    
            except json.JSONDecodeError:
                continue

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 parser.py <input_log.json> [output_filename.md]")
        sys.exit(1)
        
    input_log = sys.argv[1]
    output_md = sys.argv[2] if len(sys.argv) > 2 else "human_readable_chat.md"
    
    parse_copilot_stream(input_log, output_md)
    print(f"Success! Cleaned chat saved to '{output_md}'")

