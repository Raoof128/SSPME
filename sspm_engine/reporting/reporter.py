from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from ..models import ScanResult


class Reporter:
    def __init__(self, template_dir: str):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.env.globals["now"] = lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_markdown_report(self, result: ScanResult, output_path: str):
        template = self.env.get_template("report.md.j2")
        content = template.render(
            score=result.score, findings=result.findings, counts=result.counts
        )
        with open(output_path, "w") as f:
            f.write(content)

    def generate_json_report(self, result: ScanResult, output_path: str):
        # Pydantic models have a .dict() method (v1) or .model_dump() (v2)
        # Assuming Pydantic v1 compatibility based on requirements
        # often defaulting to older strictness. Best to use json()

        with open(output_path, "w") as f:
            f.write(result.json(indent=2))
