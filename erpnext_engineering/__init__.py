import frappe

__version__ = "1.0.0"

def get_engineering_settings():
    """
    Get engineering settings and configurations
    Returns:
        dict: Engineering settings
    """
    return frappe.get_single("Engineering Settings")

def get_project_types():
    """
    Get list of engineering project types
    Returns:
        list: A list of project type names
    """
    return frappe.db.get_all('Engineering Project Type', pluck='name', order_by='name asc')