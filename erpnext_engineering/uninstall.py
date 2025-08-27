import click

from erpnext_engineering.setup import before_engineering_app_uninstall as uninstall_engineering_app


def before_engineering_uninstall():
	try:
		print("Removing customizations created by the Engineering module...")
		uninstall_engineering_app()

	except Exception as e:
		BUG_REPORT_URL = "https://github.com/teodoropiccinni.com/erpnext_engineering/issues/new"
		click.secho(
			"Removing Customizations for Engineering Module failed due to an error."
			" Please try again or"
			f" report the issue on {BUG_REPORT_URL} if not resolved.",
			fg="bright_red",
		)
		raise e

	click.secho("Engineering app customizations have been removed successfully...", fg="green")
