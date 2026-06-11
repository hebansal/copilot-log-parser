import json
import sys
import os

def parse_copilot_stream(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        outfile.write("# Parsed Copilot Chat Session\n\n")
        
        for line in infile:
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    continue

                # 1. Extract User prompt text
                if "k" in data and isinstance(data["k"], list) and "inputText" in data["k"]:
                    outfile.write(f"\n### 👤 User\n> {data.get('v', '')}\n\n")
                
                # 2. Extract Assistant response snippets and inline references
                if data.get("kind") == 2:
                    v_data = data.get("v", [])
                    
                    if isinstance(v_data, list):
                        responses = v_data
                    elif isinstance(v_data, dict):
                        requests = v_data.get("requests", [])
                        responses = []
                        if isinstance(requests, list):
                            for req in requests:
                                if isinstance(req, dict):
                                    responses.extend(req.get("response", []))
                    else:
                        responses = []

                    # Process response stream items in exact sequential order
                    for resp in responses:
                        if not isinstance(resp, dict):
                            continue
                        
                        # Handle thinking blocks
                        if resp.get("kind") == "thinking" and resp.get("value"):
                            val = resp["value"]
                            outfile.write(f"#### 🧠 Copilot Thoughts\n*{val.strip()}*\n\n")
                        
                        # Handle standard markdown text chunks
                        elif resp.get("value"):
                            outfile.write(resp["value"])
                        
                        # Handle interactive file / symbol references
                        elif "inlineReference" in resp:
                            ref = resp["inlineReference"]
                            if not isinstance(ref, dict):
                                continue
                            
                            # Case A: Named function/variable reference
                            if "name" in ref:
                                outfile.write(f" `{ref['name']}` ")
                            
                            # Case B: Direct file system path reference
                            elif "fsPath" in ref:
                                full_path = ref["fsPath"]
                                # General truncation logic for any user project path
                                if "backend" in full_path.lower():
                                    relative_path = full_path.split("/")[-2] + "/" + full_path.split("/")[-1]
                                else:
                                    relative_path = os.path.basename(full_path)
                                outfile.write(f" `{relative_path}` ")
                                    
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

