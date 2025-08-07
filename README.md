<div align="center">
	<a href="https://www.teodoropiccinni.com/erpnext/engineering">
		<img src=".github/engineering_logo.png" height="80px" width="80px" alt="Engineering Logo">
	</a>
	<h2>Car Workshop</h2>
	<p align="center">
		<p>Open Source, modern, and easy-to-use Engineering Software for ERPnext</p>
	</p>

[![codecov](https://codecov.io/gh/frappe/hrms/branch/develop/graph/badge.svg?token=0TwvyUg3I5)](https://codecov.io/gh/frappe/hrms)


# Engineering

Engineering module to provide advanced fucntionalities and custom configurations for engineering teams.

## Functionalities
* Item coding based on Naming Series
* Naming Series dictionary (Item Coding Table)
* Item Revisions

### Production
```
SITE=sitename
bench new-site $SITE
```

1. Install Car Workshop App
You can install this app using the [bench](https://github.com/frappe/bench) CLI:
```bash
PATH_TO_YOUR_BENCH="~/frappe-bench/"
URL_OF_THIS_REPO="git@github.com:teodoropiccinni/erpnext_engineering.git"
VERSION_OF_FRAPPE="version-15"
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch $VERSION_OF_FRAPPE
bench --site $SITE install-app erpnext_engineering
```
Where `$PATH_TO_YOUR_BENCH` is usually: `~/frappe-bench/` and `version-15` is the current version. Adapt those parameters to your needs.

2. Disable developer mode
```
bench --site yoursite set-config -g developer_mode 0
```



### Development
```
SITE=sitename
bench new-site $SITE
```

1. Install Car Workshop App
You can install this app using the [bench](https://github.com/frappe/bench) CLI:
```bash
PATH_TO_YOUR_BENCH="~/frappe-bench/"
URL_OF_THIS_REPO="git@github.com:teodoropiccinni/erpnext_engineering.git"
VERSION_OF_FRAPPE="develop-15"
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch $VERSION_OF_FRAPPE
bench --site $SITE install-app erpnext_engineering
```
Where `$PATH_TO_YOUR_BENCH` is usually: `~/frappe-bench/` and `version-15` is the current version. Adapt those parameters to your needs.

2. Enable developer mode
```
bench --site yoursite set-config -g developer_mode 1
```





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

