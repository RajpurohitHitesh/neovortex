import click
from .client import NeoVortexClient
from .exceptions import NeoVortexError

@click.group()
def cli():
    """NeoVortex CLI for quick API testing."""
    pass

@cli.command()
@click.option("--method", default="GET", help="HTTP method")
@click.option("--url", required=True, help="Target URL")
@click.option("--headers", multiple=True, help="Headers as key=value")
def request(method: str, url: str, headers: list):
    """Send an HTTP request."""
    try:
        header_dict = dict(h.split("=") for h in headers)
        with NeoVortexClient() as client:
            response = client.request(method, url, headers=header_dict)
            click.echo(f"Status: {response.status_code}")
            click.echo(f"Response: {response.text}")
    except NeoVortexError as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == "__main__":
    cli()