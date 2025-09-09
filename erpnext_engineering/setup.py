import os
import time
import json


from erpnext_engineering.tools.erpnext_tpdev_helper.erpnext_tpdev_setup_helper import ERPnext_TPdev_SetupHelper
import frappe

TPH = ERPnext_TPdev_SetupHelper(
    app_name="erpnext_engineering",
    module_name="Engineering",
    module_profile_name="Engineering Profile",
    workspace_name="Engineering",
    workspace_label="Engineering",
    workspace_title="Engineering",
    workspace_icon="list-alt",
    workspace_for_user="",
    workspace_indicator_color="blue",
    workspace_is_hidden="0",
    workspace_parent_page="",
    workspace_public=True,
    workspace_sequence_id=2.2,
    workspace_files = {
        "folder": "../apps/erpnext_engineering/erpnext_engineering/engineering/workspace/engineering",
        "content": "content.json",
        "content_blocks": "content_blocks.json",
        "links": "links.json",
        "number_cards": "number_cards.json",
        "shortcuts": "shortcuts.json"
    },
    client_scripts=[
        {
            "name": "engineering_script_item_item_coding_table_prefix_check_form",
            "file": "engineering_script_item_item_coding_table_prefix_check.js",
            "folder": "../apps/erpnext_engineering/erpnext_engineering/engineering/client_script",
            "type": "Form",
            "doctype": "Item"
        },
        {
            "name": "engineering_script_item_item_coding_table_prefix_check_list",
            "file": "engineering_script_item_item_coding_table_prefix_check.js",
            "folder": "../apps/erpnext_engineering/erpnext_engineering/engineering/client_script",
            "type": "List",
            "doctype": "Item"
        },
    ],
    email_groups = [
        {
            "name": "Engineering Team",
            "title": "Engineering Team",
            "description": "Email group for the Engineering team"
        },
        {
            "name": "Logistic Team",
            "title": "Logistic Team",
            "description": "Email group for the Logistic team"
        }
    ],
    roles_list = [
        "Engineering Manager",
        "Engineering User",
        "Engineering Viewer",
        "Logistic Manager",
        "Logistic User"
    ],
    roles_profile_module = [
        {
            "profile": "Engineering Manager Profile",
            "roles": [
                "Employee",
                "Engineering Manager",
                "Logistic Manager",
                "Stock Manager",
                "Projects Manager",
                "Purchase Manager"
            ],
            "modules": [
                "Engineering",
                "Quality Management",
                "Stock",
                "Manufacturing",
                "Projects",
                "Buying",
                "Contacts",
                "Core"
            ]
        },
        {
            "profile": "Engineering User Profile",
            "roles": [
                "Employee",
                "Engineering User",
                "Logistic User",
                "Stock User",
                "Projects User",
                "Purchase User"
            ],
            "modules": [
                "Engineering",
                "Quality Management",
                "Stock",
                "Manufacturing",
                "Projects",
                "Buying",
                "Contacts",
                "Core"
            ]
        },
        {
            "profile": "Engineering Viewer Profile",
            "roles": [
                "Employee",
                "Engineering Viewer"
            ],
            "modules": [
                "Engineering"
                "Stock",
                "Manufacturing",
                "Projects",
                "Buying",
                "Contacts",
                "Core"
            ]
        },
        {
            "profile": "Logistic Manager Profile",
            "roles": [
                "Employee",
                "Engineering Manager",
                "Logistic Manager",
                "Stock Manager",
                "Projects Manager",
                "Purchase Manager"
            ],
            "modules": [
                "Engineering",
                "Quality Management",
                "Stock",
                "Manufacturing",
                "Projects",
                "Buying",
                "Contacts",
                "Core"
            ]
        },
        {
            "profile": "Logistic User Profile",
            "roles": [
                "Employee",
                "Engineering User",
                "Logistic User",
                "Stock User",
                "Projects User",
                "Purchase User"
            ],
            "modules": [
                "Engineering",
                "Quality Management",
                "Stock",
                "Manufacturing",
                "Projects",
                "Buying",
                "Contacts",
                "Core"
            ]
        }
    ],
    db_constraints = [
        {
            "doctype": "Item Revision",
            "name": "engineering_item_revision_unique_tuple",
            "constraint": [
                "engineering_item_revision_item_id",
                "engineering_item_revision_revision"
            ]
        }
    ]
)


def after_engineering_app_install():
    print("Running after_install function.")
    if(TPH.DEVELOPMENT_MODE_ON):
        cwd = os.getcwd()
        print(f"Running in path: {cwd}")

    # Install Module Def
    TPH.install_module_def()

    # Install Workspace
    TPH.install_workspace()

    # Install Roles for Engineering
    TPH.install_roles()

    # Add Module Profile
    TPH.install_module_profiles()

    # Adding Role Profiles
    TPH.install_role_profiles()

    # TODO add more detail permissions (rwde)

    # Client scripts
    TPH.install_client_scripts()

    # Create Email Group for Engineering
    TPH.install_email_groups()

    # Custom DB constraints
    TPH.install_db_constraints()

def after_engineering_app_migrate():
    # Update Workspace
    TPH.update_workspace()
    # Custom DB constraints
    TPH.install_db_constraints()



def before_engineering_app_uninstall():
    # Delete Client Scripts
    TPH.uninstall_client_scripts()
 
    # Delete Property Setters
    TPH.uninstall_property_setters_by_module()

    # Deleting Custom Fields for Engineering
    TPH.uninstall_custom_fields_by_module()

    # Deleting Roles for Engineering
    TPH.uninstall_roles()

    # Deleting Role Profiles for Engineering
    TPH.uninstall_role_profiles()
 
    # Deleting DocTypes for Engineering
    TPH.uninstall_doctypes_by_module()

    # Uninstall Workspace
    TPH.uninstall_workspace()

    # Uninstall Module Def
    TPH.uninstall_module_def()

    # Delete Module Profile
    TPH.uninstall_module_profiles()

    # Delete Email Group
    TPH.uninstall_email_groups()

    # Delete DB constraints
    TPH.uninstall_db_constraints()


#TODO: Install/Delete role permissions on DocTypes
