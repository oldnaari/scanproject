import click


def display_motivation(motivation: str):

    is_code_snippet = False

    for line in motivation.splitlines(keepends=False):
        if line.startswith("```"):
            is_code_snippet = not is_code_snippet
            continue

        color = "bright_white" if is_code_snippet else "white"
        click.echo(click.style(f"\t{line}", fg=color))


