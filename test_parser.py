import os
import unittest
from parser import extract_user_prompt, format_inline_reference, parse_copilot_stream

class TestCopilotParser(unittest.TestCase):
    
    def test_user_prompt_extraction(self):
        sample = {"kind": 1, "k": ["inputState", "inputText"], "v": "Hello world"}
        self.assertIn("Hello world", extract_user_prompt(sample))
        self.assertIn("👤 User", extract_user_prompt(sample))

    def test_inline_reference_symbol(self):
        sample = {"name": "bcrypt.hashSync()"}
        self.assertEqual(format_inline_reference(sample), " `bcrypt.hashSync()` ")

    def test_inline_reference_file_path(self):
        sample = {"fsPath": "/home/user/backend/src/db.js"}
        self.assertEqual(format_inline_reference(sample), " `src/db.js` ")

    def test_full_pipeline_execution(self):
        # Run real file parsing test
        input_file = "test_sample.jsonl"
        output_file = "test_output.md"
        
        if os.path.exists(input_file):
            parse_copilot_stream(input_file, output_file)
            self.assertTrue(os.path.exists(output_file))
            
            with open(output_file, "r") as f:
                content = f.read()
                self.assertIn("👤 User", content)
                self.assertIn("JSON.stringify()", content)
                self.assertIn("cache/index.js", content)
                
            # Clean up test artifact
            os.remove(output_file)

if __name__ == "__main__":
    unittest.main()

