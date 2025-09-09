#!/bin/bash

echo "-------------MODULE UPDATE SCRIPT-------------"
echo "Execution started at: $(date)"
: "${SITE:?Set SITE variable}"
echo "Site: $SITE"
: "${APP_NAME:?Set APP_NAME variable}"
echo "App Name: $APP_NAME"
echo "----------------------------------------------"
echo ""
echo "Updating GIT repository and submodules..."
git pull
if [ $? -eq 0 ]; then
  echo "- GIT repo update successful"
else
  echo "- GIT repo update failed"
  exit 1
fi
git pull --recurse-submodules
if [ $? -eq 0 ]; then
  echo "- GIT submodule update successful"
else
  echo "- GIT submodule update failed"
  exit 1
fi
echo ""
echo "Checking Frappe Bench version..."
bench --version
if [ $? -eq 0 ]; then
  echo "- Frappe Bench version check successful"
else
  echo "- Frappe Bench version check failed. Is it python available or are you running in the correct virtualenv?"
  exit 1
fi
echo ""
echo "Updating Frappe app: $APP_NAME"
echo "- Uninstalling Frappe app: $APP_NAME"
bench --site $SITE uninstall-app $APP_NAME
if [ $? -eq 0 ]; then
  echo "- - Frappe app: $APP_NAME uninstall successful"
else
  echo "- - Frappe app: $APP_NAME uninstall failed"
fi
echo ""
echo "Clearing cache..."
bench --site $SITE clear-cache
echo ""
echo "- Installing Frappe app: $APP_NAME"
bench --site $SITE install-app $APP_NAME
if [ $? -eq 0 ]; then
  echo "- - Frappe app: $APP_NAME install successful"
else
  echo "- - Frappe app: $APP_NAME install failed"
fi

echo "Update completed at: $(date)"
echo "-------------MODULE UPDATE SCRIPT-------------"