from __future__ import annotations
from pathlib import Path

import typer
import re
import yaml

app = typer.Typer(add_completion=False, no_args_is_help=True, help="Vendor Hub CLI")
VENDORS_DIR = Path(__file__).parent / "vendors"
__version__ = "0.1.0"



# Vendors group
vendors_app = typer.Typer(help="Manage vendor configuration")

@vendors_app.command("list")
def vendors_list():
    """List known vendors."""
    # List the vendor files
    for yml_path in sorted(VENDORS_DIR.glob("*.yaml")):
        if yml_path.name.startswith("_"):
            continue
        # Load the vendor data
        try:
            data = yaml.safe_load(yml_path.read_text(encoding="utf-8")) or {}
            slug = data.get("slug", yml_path.stem)
            base = data.get("base_url", "")
            tos = data.get("tos_url", "")
            # Print the vendor data
            typer.echo(f"{slug}: {base} ({tos})")
        # Print any errors
        except Exception as e:
            typer.echo(f"Error loading {yml_path}: {e}")

@vendors_app.command("show")
def vendors_show(slug: str = typer.Argument(..., help="Vendor slug")):
    """Show one vendor."""
    # Check if the vendor exists
    yml_path = VENDORS_DIR / f"{slug}.yaml"
    if not yml_path.exists():
        typer.echo(f"Vendor {slug} not found")
        raise typer.Exit(code=1)
    
    # Load the vendor data
    data = yaml.safe_load(yml_path.read_text(encoding="utf-8")) or {}
    typer.echo(yaml.safe_dump(data, sort_keys=False))

@vendors_app.command("add")
def vendors_add(
        slug: str = typer.Argument(..., help="Vendor slug"),
        base_url: str = typer.Option(..., "--base-url"),
        tos_url: str = typer.Option("", "--tos-url"),
        login_url: str = typer.Option("", "--login-url"),
        username_env: str = typer.Option(None, "--username-env"),
        password_env: str = typer.Option(None, "--password-env"),
        ):
    """Add a new vendor with the given slug and base URL."""
    typer.echo(f"Adding vendor: {slug}")

    # Validate the slug
    if not re.fullmatch(r"[A-Za-z0-9_-]+", slug):
        typer.echo(f"Invalid slug: {slug}. Use letters, numbers, underscores, or hyphens only.")
        raise typer.Exit(code=1)
    
    # Check if the vendor already exists
    out_path = VENDORS_DIR / f"{slug}.yaml"
    if out_path.exists():
        typer.echo(f"Vendor {slug} already exists {out_path}")
        raise typer.Exit(code=2)
    
    # Generate the environment variable names
    slug_upper = slug.upper().replace("-", "_")
    username_env = username_env or f"{slug_upper}_USERNAME"
    password_env = password_env or f"{slug_upper}_PASSWORD"    
    
    # Generate the new vendor data
    new_data = {
        "slug": slug,
        "base_url": base_url,
        "start_urls": [base_url],
        "tos_url": tos_url or None,
        "login": {
            "login_url": login_url or None,
            "username_env": username_env or f"VENDOR_{slug_upper}_USERNAME",
            "password_env": password_env or f"VENDOR_{slug_upper}_PASSWORD",
            "username_selector": "input[name='username']",
            "password_selector": "input[name='password']",
            "submit_selector": "button[type='submit']",
        }
    }

    # Write the new vendor data to a YAML file
    out_path.write_text(yaml.safe_dump(new_data, sort_keys=False), encoding="utf-8")
    typer.echo(f"Vendor {slug} added to {out_path}")

@vendors_app.command("remove")
def vendors_remove(slug: str = typer.Argument(..., help="Vendor slug"), force: bool = typer.Option(False, "--force")):
    """Remove a vendor."""
    yml_path = VENDORS_DIR / f"{slug}.yaml"

    # Check if the vendor exists
    if not yml_path.exists():
        typer.echo(f"Vendor {slug} not found")
        raise typer.Exit(code=1)
    
    # Confirm the removal (unless --force is used)
    if not force and not typer.confirm(f"Are you sure you want to remove {slug}?"):
        typer.echo("Aborted")
        raise typer.Exit(code=2)
    
    # Remove the vendor file
    yml_path.unlink()
    typer.echo(f"Vendor {slug} removed")

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
def scrape_run(
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