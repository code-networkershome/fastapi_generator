from jinja2 import Environment, FileSystemLoader
import os
from .models import CPS

TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def generate_project(cps: CPS) -> dict:
    files = {}
    
    # List of templates to render
    templates = [
        ("app/main.py.jinja", f"{cps.project_name}/app/main.py"),
        ("app/core/llm.py.jinja", f"{cps.project_name}/app/core/llm.py"),
        ("app/schemas.py.jinja", f"{cps.project_name}/app/schemas.py"),
        ("app/__init__.py.jinja", f"{cps.project_name}/app/__init__.py"),
        ("requirements.txt.jinja", f"{cps.project_name}/requirements.txt"),
        ("README.md.jinja", f"{cps.project_name}/README.md"),
        (".env.example.jinja", f"{cps.project_name}/.env.example"),
    ]

    if cps.mode == "rag_only":
        templates += [
            ("app/api/ingest.py.jinja", f"{cps.project_name}/app/api/ingest.py"),
            ("app/api/query.py.jinja", f"{cps.project_name}/app/api/query.py"),
            ("app/core/vector_store.py.jinja", f"{cps.project_name}/app/core/vector_store.py"),
        ]
    else:
        templates += [
            ("app/api/chat.py.jinja", f"{cps.project_name}/app/api/chat.py"),
        ]
    
    # Dynamic modules
    for module in cps.modules:
        templates.append(("app/api/module.py.jinja", f"{cps.project_name}/app/api/{module}.py", {"module": module}))
    
    for template_info in templates:
        if len(template_info) == 2:
            template_path, output_path = template_info
            context = {"cps": cps.model_dump()}
        else:
            template_path, output_path, extra_context = template_info
            context = {"cps": cps.model_dump(), **extra_context}

        try:
            template = env.get_template(template_path)
            rendered = template.render(**context)
            files[output_path] = rendered
        except Exception as e:
            # If a template is optional or missing features, handle it
            # For now, if chat feature is false, we might skip chat.py
            if "chat.py" in template_path and not cps.features.chat:
                continue
            # If rag feature is false, we might change llm.py content (handled in jinja)
            
            # For __init__.py which might be empty
            if "__init__.py" in template_path:
                files[output_path] = ""
                continue
                
            print(f"Error rendering {template_path}: {e}")
            
    return files
