from frappe import _

def get_data():
    return [
        {
            "module_name": "Car Workshop",
            "category": "Modules",
            "label": _("Car Workshop"),
            "icon": "octicon octicon-milestone",
            "color": "blue",
            "type": "module",
            "description": "Engineering module to provide advanced fucntionalities and custom configurations for engineering teams."
        }
    ]

