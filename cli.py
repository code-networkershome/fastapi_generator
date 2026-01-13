import requests
import json
import os
import argparse
import sys

BASE_URL = "http://localhost:8000"
API_KEY = "fastapi-gen-secret"

def generate_project(idea, output_dir=None):
    print(f"🚀 Generating project for: {idea}")
    url = f"{BASE_URL}/api/v1/generate"
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": API_KEY
    }
    payload = {"idea": idea}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        project_name = data.get("project_name", "generated_project")
        files = data.get("files", {})
        
        target_dir = output_dir or project_name
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        for path, content in files.items():
            # Extract only the path after the project name if present
            # The backend currently returns paths like 'ProjectName/app/main.py'
            relative_path = path.replace(f"{project_name}/", "", 1)
            full_path = os.path.join(target_dir, relative_path)
            
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        
        print(f"✅ Project generated successfully in: {os.path.abspath(target_dir)}")
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error: {e.response.json().get('detail', str(e))}")
    except Exception as e:
        print(f"❌ Failed to generate project: {e}")

def main():
    parser = argparse.ArgumentParser(description="FastAPI Generator CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    generate_parser = subparsers.add_parser("generate", help="Generate a new project")
    generate_parser.add_argument("idea", help="Project idea or description")
    generate_parser.add_argument("--out", "-o", help="Output directory")

    args = parser.parse_args()
    
    if args.command == "generate":
        generate_project(args.idea, args.out)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
