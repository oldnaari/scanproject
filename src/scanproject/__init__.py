import click
import openai
import pathlib
from . import config

from .display_motivation import display_motivation


@click.group()
def main():
    pass


@main.command()
@click.option("--api-key", default=None, help="The API Key")
@click.option("--model", default=None, help="The model to use")
def activate(api_key, model):
    config_dict = config.load()

    if api_key is not None:
        config_dict["api_key"] = api_key

    config.save(config_dict)


@main.command()
@click.argument("query")
@click.option("--directory",
              default=".",
              help='The directory to scan recursively'
              )
@click.option("-r", "--report",
              is_flag=True,
              help="Displays the results as a detailed report")
def find(query, directory, report):
    cwd = pathlib.Path(__file__).parent
    config_path = cwd / "config.json"

    config_dict = config.load()

    if "api_key" not in config_dict:
        click.echo(click.style("Api key not provided, to provide the key please use:", fg="bright_red", bold=True))
        click.echo(click.style("    scanproject activate --api-key <your-api-key>", fg="bright_white"))
        return

    openai.api_key = config_dict["api_key"]

    directory = pathlib.Path(directory)

    if report:
        click.echo(click.style(f"Checking the query '{query}'", fg="green"))
        click.echo(click.style("Matching files", fg="green", bold=True))
        match_prefix = "    "
    else:
        match_prefix = ""

    matching_files = []

    for path in directory.glob("**/*"):
        if not path.is_file():
            continue

        try:
            with open(path, "r") as fp:
                file_contents = fp.read()
        except UnicodeDecodeError:
            continue

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": f"""You will receive messages with first line being 
                 the path to a file, and the rest of the message its contents. 
                 You should check whether the file suffices to the query "{str(query)}".
                 f"Your answer should be only a single word either 'yes' or 'no' without any other symbols"
                 """
                 },
                {"role": "user",
                 "content": f"{str(path)}\n{file_contents}"}
            ],
            temperature=0.0,
            max_tokens=1000,
        )
        # click.echo(response)
        answer = response["choices"][0]["message"]["content"]
        # click.echo(f"{answer}\t: {path}")

        if answer.lower() == "yes":
            matching_files.append(path)
            click.echo(click.style(match_prefix + str(path), fg="green"))


    if not report:
        return

    for path in matching_files:
        try:
            with open(path, "r") as fp:
                file_contents = fp.read()
        except UnicodeDecodeError:
            continue

        click.echo("\n")
        click.echo(click.style(f"{path}", fg="yellow", bold=True))

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": f"""You will receive messages with first line being 
                 the path to a file, and the rest of the message its contents. 
                 Please write why the files suffices the query "{str(query)}". 
                 Also provide the fragment in the file that proves your point in triple backticks (if there is any).
                 """
                 },
                {"role": "user",
                 "content": f"{str(path)}\n{file_contents}"}
            ],
            temperature=0.0,
            max_tokens=1000,
        )
        motivation = response["choices"][0]["message"]["content"]
        display_motivation(motivation)
