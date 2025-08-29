import click

from erpnext_engineering.setup import after_engineering_app_migrate as migrate_engineering_app


def after_engineering_migrate():
	try:
		print("Migrating Engineering module...")
		migrate_engineering_app()

		click.secho("Thank you for updating Engineering module for ERPnext!", fg="green")

	except Exception as e:
		BUG_REPORT_URL = "https://github.com/teodoropiccinni.com/erpnext_engineering/issues/new"
		click.secho(
			"Migration for app failed due to an error."
			" Please try re-installing the app or"
			f" report the issue on {BUG_REPORT_URL} if not resolved.",
			fg="bright_red",
		)
		raise e


