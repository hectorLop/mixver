from typing import List

from rich.console import Console
from rich.table import Table


def show_tags(
    tags: List[str], names: List[str], versions: List[str], paths: List[str]
) -> None:
    """
    Display the tags data in the CLI.
    """
    table = Table(title="Artifacts")

    table.add_column("Tag", justify="center", style="green")
    table.add_column("Name", justify="center", style="black")
    table.add_column("Version", justify="center", style="cyan")
    table.add_column("Path", justify="center", style="red")

    for i, tag in enumerate(tags):
        table.add_row(tag, names[i], versions[i], paths[i])

    console = Console()
    console.print(table)
