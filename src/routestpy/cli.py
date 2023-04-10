from pathlib import Path

import click
from jinja2 import Environment
from jinja2 import FileSystemLoader


@click.group()
def cli():
    """Routestpy CLI is just awesome."""


@cli.command()
@click.option(
    '--project-dir',
    type=click.Path(exists=True, file_okay=False, writable=True),
    default=".",
    help="The project directory path. Default is the current directory.",
)
@click.option('--project-name', type=str, required=True, help="The name of the new project.")
def new_project(project_dir: Path, project_name: str) -> None:
    """Create a new Routestpy project."""
    project_dir = Path(project_dir)
    if not project_dir:
        project_dir = Path.cwd()

    if (project_dir / project_name).exists():
        click.echo(f"Error: The project '{project_name}' already exists in '{project_dir}'.")
        return

    if not click.confirm(f"Do you want to create a new project '{project_name}' in '{project_dir}'?", abort=True):
        return

    (project_dir / project_name / "app").mkdir(parents=True, exist_ok=True)
    (project_dir / project_name / "config").mkdir(parents=True, exist_ok=True)
    (project_dir / project_name / "routes").mkdir(parents=True, exist_ok=True)

    env = Environment(loader=FileSystemLoader(str(Path(__file__).parent / 'templates')))
    app_template = env.get_template('app.j2')
    app_yaml_template = env.get_template('app_yaml.j2')
    qa_yaml_template = env.get_template('qa_yaml.j2')
    stage_yaml_template = env.get_template('stage_yaml.j2')
    prod_yaml_template = env.get_template('prod_yaml.j2')
    runner_template = env.get_template('runner.j2')

    with click.progressbar(length=6, label="Creating files...") as bar:
        (project_dir / project_name / "app" / "__init__.py").touch()
        bar.update(1)

        with open(project_dir / project_name / "app" / "app.py", 'w') as f:
            f.write(app_template.render(project_name=project_name))
        bar.update(1)

        with open(project_dir / project_name / "app" / "app.yaml", 'w') as f:
            f.write(app_yaml_template.render(project_name=project_name))
        bar.update(1)

        with open(project_dir / project_name / "config" / "qa.yaml", 'w') as f:
            f.write(qa_yaml_template.render())
        bar.update(1)

        with open(project_dir / project_name / "config" / "stage.yaml", 'w') as f:
            f.write(stage_yaml_template.render())
        bar.update(1)

        with open(project_dir / project_name / "config" / "prod.yaml", 'w') as f:
            f.write(prod_yaml_template.render())
        bar.update(1)

        with open(project_dir / project_name / "routes" / "__init__.py", 'w') as f:
            f.write("")

        with open(project_dir / project_name / "runner.py", 'w') as f:
            f.write(runner_template.render())

    click.echo(f"New project '{project_name}' created successfully in '{project_dir}'.")


if __name__ == "main":
    cli()
