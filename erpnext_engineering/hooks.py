app_name = "erpnext_engineering"
app_title = "ERPNext Engineering"
app_publisher = "Teodoro P."
app_description = "ERPNext Engineering module providing comprehensive engineering management features including project planning, resource allocation, technical documentation, and engineering workflows for manufacturing and construction projects."
app_email = "teodoropiccinni@example.com"
app_license = "MIT"

# Apps
# ------------------

required_apps = ["erpnext"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnext_engineering/css/erpnext_engineering.css"
# app_include_js = "/assets/erpnext_engineering/js/erpnext_engineering.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpnext_engineering/css/erpnext_engineering.css"
# web_include_js = "/assets/erpnext_engineering/js/erpnext_engineering.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# after_install = "erpnext_engineering.setup.install.setup"

# Uninstallation
# ------------

# before_uninstall = "erpnext_engineering.uninstall.before_uninstall"
# after_uninstall = "erpnext_engineering.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnext_engineering.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"erpnext_engineering.tasks.all"
# 	],
# 	"daily": [
# 		"erpnext_engineering.tasks.daily"
# 	],
# 	"hourly": [
# 		"erpnext_engineering.tasks.hourly"
# 	],
# 	"weekly": [
# 		"erpnext_engineering.tasks.weekly"
# 	],
# 	"monthly": [
# 		"erpnext_engineering.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "erpnext_engineering.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "erpnext_engineering.event.get_events"
# }

# Automatically update python controller files with type annotations for this app.
export_python_type_annotations = True