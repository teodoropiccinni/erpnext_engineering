import click

from erpnext_engineering.setup import after_install as setup


def after_install():
	try:
		print("Setting up Car Workshop...")
		setup()

		click.secho("Thank you for installing Car Workshop module for ERPnext!", fg="green")

	except Exception as e:
		BUG_REPORT_URL = "https://github.com/teodoropiccinni.com/erpnext_engineering/issues/new"
		click.secho(
			"Installation for Car Workshop app failed due to an error."
			" Please try re-installing the app or"
			f" report the issue on {BUG_REPORT_URL} if not resolved.",
			fg="bright_red",
		)
		raise e
