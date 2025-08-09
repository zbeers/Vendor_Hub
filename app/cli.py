from __future__ import annotations

import typer

app = typer.Typer(add_completion=False, no_args_is_help=True, help="Vender Hub CLI")
__version__ = "0.1.0"

# Vendors group
vendors_app = typer.Typer(help="Manage vendor configuration")

@vendors_app.command("list")
def vendors_list():
    """List known vendors (stub). """
    typer.echo("Vendors: (none yet)")

@vendors_app.command("show")
def vendors_show(slug: str = typer.Argument(..., help="Vendor slug")):
    """Show one vendor (stub)."""
    typer.echo(f"Vendor: {slug}")

@vendors_app.command("add")
def vendors_add(slug: str = typer.Argument(..., help="Vendor slug")):
    """Add a new vendor (stub)."""
    typer.echo(f"Adding vendor: {slug}")

@vendors_app.command("remove")
def vendors_remove(slug: str = typer.Argument(..., help="Vendor slug")):
    """Remove a vendor (stub)."""
    typer.echo(f"Removing vendor: {slug}")

@vendors_app.command("edit")
def vendors_edit(slug: str = typer.Argument(..., help="Vendor slug")):
    """Edit a vendor (stub)."""
    typer.echo(f"Editing vendor: {slug}")


app.add_typer(vendors_app, name="vendors")

# Compliance group
tos_app = typer.Typer(help="Compliance checks (TOS and robots.txt)")
@tos_app.command("check")
def tos_check(slug: str = typer.Argument(..., help="Vendor slug")):
    """Check TOS and robots.txt for vendor (stub)."""
    typer.echo(f"Check TOS/robots for: {slug}")

app.add_typer(tos_app, name="tos")

# Authentication group
auth_app = typer.Typer(help="Authentication workflows")

@auth_app.command("login")
def auth_login(slug: str = typer.Argument(..., help="Vendor slug")):
    """Try login for a vendor (stub)."""
    typer.echo(f"Attempting login for: {slug}")

app.add_typer(auth_app, name="auth")

# Scraping group
scrape_app = typer.Typer(help="Scraping workflows")

@scrape_app.command("run")
def scrap_run(
        slug: str = typer.Argument(..., help="Vendor slug"),
        page: str = typer.Option("all", "--page", help="Which page ('all' or URL/index)"),
):
    """Run a scrape (stub)."""
    typer.echo(f"Scrape vendor={slug}, page={page}")

app.add_typer(scrape_app, name="scrape")

# Utilities group

@app.command("version")
def version():
    """Show CLI version"""
    typer.echo(__version__)



if __name__ == "__main__":
    app()