import yaml
from jinja2 import Template


def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_prompt(data: dict) -> str:
    return f"""
    Background:
    {data["background"]}

    Role and Goal:
    {data["role_and_goal"]}

    Task:
    {data["task"]}

    {data["query"]}
    """.strip()


def render_prompt(prompt: str) -> str:
    return Template(prompt).render()


def load_rag_prompt(prompt_path: str) -> str:
    data = load_yaml(prompt_path)
    prompt = build_prompt(data)
    return render_prompt(prompt)
