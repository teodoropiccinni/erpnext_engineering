#!/bin/bash

echo -e "\033[32m-------------MODULE UPDATE SCRIPT-------------\033[0m"
echo "Execution started at: $(date)"
: "${SITE:?Set SITE variable}"
echo "Site: $SITE"
: "${APP_NAME:?Set APP_NAME variable}"
echo "App Name: $APP_NAME"
echo -e "\033[32m----------------------------------------------\033[0m"
echo ""
echo -e "\033[34mUpdating GIT repository and submodules...\033[0m"
git pull
if [ $? -eq 0 ]; then
  echo -e "\033[32m- GIT repo update successful\033[0m"
else
  echo -e "\033[31m- GIT repo update failed\033[0m"
  exit 1
fi
git pull --recurse-submodules
if [ $? -eq 0 ]; then
  echo -e "\033[32m- GIT submodule update successful\033[0m"
else
  echo -e "\033[31m- GIT submodule update failed\033[0m"
  exit 1
fi
echo ""
echo -e "\033[34mChecking Frappe Bench version...\033[0m"
bench --version
if [ $? -eq 0 ]; then
  echo -e "\033[32m- Frappe Bench version check successful\033[0m"
else
  echo -e "\033[31m- Frappe Bench version check failed. Is it python available or are you running in the correct virtualenv?\033[0m"
  exit 1
fi
echo ""
echo -e "\033[34mUpdating Frappe app: $APP_NAME\033[0m"
echo "- Uninstalling Frappe app: $APP_NAME"
bench --site $SITE uninstall-app $APP_NAME
if [ $? -eq 0 ]; then
  echo -e "\033[32m- - Frappe app: $APP_NAME uninstall successful\033[0m"
else
  echo -e "\033[31m- - Frappe app: $APP_NAME uninstall failed\033[0m"
fi
echo ""
echo -e "\033[34mClearing cache...\033[0m"
bench --site $SITE clear-cache
echo ""
echo "- Installing Frappe app: $APP_NAME"
bench --site $SITE install-app $APP_NAME
if [ $? -eq 0 ]; then
  echo -e "\033[32m- - Frappe app: $APP_NAME install successful\033[0m"
else
  echo -e "\033[31m- - Frappe app: $APP_NAME install failed\033[0m"
fi

echo "Update completed at: $(date)"
echo -e "\033[32m-------------MODULE UPDATE SCRIPT-------------\033[0m"