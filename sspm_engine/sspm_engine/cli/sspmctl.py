import typer
from rich.console import Console
from rich.table import Table
from sspm_engine.engine import SSPMEngine
from sspm_engine.models import Severity

app = typer.Typer()
console = Console()


@app.command()
def scan(
    provider: str = typer.Argument(
        "all", help="Provider to scan: all, slack, github, google"
    )
):
    """
    Scan SaaS providers for security risks.
    """
    console.print(f"[bold green]Starting scan for {provider}...[/bold green]")

    engine = SSPMEngine()
    results = engine.run_scan(provider)

    table = Table(title="Scan Results")
    table.add_column("Severity", style="bold")
    table.add_column("Rule", style="cyan")
    table.add_column("Resource", style="magenta")
    table.add_column("Details")

    for finding in results.findings:
        severity_color = (
            "red"
            if finding.severity == Severity.CRITICAL
            else "yellow" if finding.severity == Severity.HIGH else "blue"
        )
        table.add_row(
            f"[{severity_color}]{finding.severity.value}[/{severity_color}]",
            finding.rule_id,
            finding.resource_id,
            finding.details,
        )

    console.print(table)
    console.print(f"\n[bold]Risk Score:[/bold] {results.score}/100")
    console.print(f"[bold]Summary:[/bold] {results.counts}")


@app.command()
def report(format: str = "markdown", output: str = "report.md"):
    """
    Generate a security report.
    """
    engine = SSPMEngine()
    results = engine.run_scan("all")
    engine.generate_report(results, format, output)
    console.print(f"[bold green]Report generated at {output}[/bold green]")


@app.command()
def risk_score():
    """
    Calculate and display the current risk score.
    """
    engine = SSPMEngine()
    results = engine.run_scan("all")
    console.print(f"[bold]Current Risk Score:[/bold] {results.score}")


if __name__ == "__main__":
    app()
