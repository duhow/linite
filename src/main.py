import click
import yaml
from package import Package

@click.group()
def cli():
    pass

@click.command()
@click.argument('package')
def install(package):
    click.echo(f"installing {package=}")


@click.command()
@click.argument('file')
def bootstrap(file):
    click.echo(f"installing packages from {file=}")
    yaml_data = None
    with open(file, "r") as yaml_file:
        yaml_data = yaml.safe_load(yaml_file.read())

    for entry in yaml_data:
        pkg = Package(entry)
        print(pkg.name)
    

cli.add_command(install)
cli.add_command(bootstrap)

if __name__ == '__main__':
    cli()