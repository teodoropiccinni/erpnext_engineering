# Engineering

Engineering module to provide advanced fucntionalities and custom configurations for engineering teams.




### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
PATH_TO_YOUR_BENCH="~/frappe-bench/"
URL_OF_THIS_REPO="git@github.com:teodoropiccinni/erpnext_engineering.git"
VERSION_OF_FRAPPE="version-15"
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch $VERSION_OF_FRAPPE
bench install-app erpnext_engineering
```
Where `$PATH_TO_YOUR_BENCH` is usually: `~/frappe-bench/` and `version-15` is the current version. Adapt those parameters to your needs.

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/erpnext_engineering
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.

## License

mit

## External resources
* Installation: 
* Enable HTTPS: https://docs.frappe.io/framework/user/en/bench/guides/configuring-https
* Server Script API: 
* Client Script API: https://docs.frappe.io/framework/user/en/api/form

* Icons: https://primer.github.io/octicons/

