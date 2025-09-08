#!/bin/bash

git pull
if [ $? -eq 0 ]; then
  echo "GIT repo update successful"
else
  echo "GIT repo update failed"
  exit 1
fi
git pull --recurse-submodules
if [ $? -eq 0 ]; then
  echo "GIT submodule update successful"
else
  echo "GIT submodule update failed"
  exit 1
fi

bench --site $SITE uninstall-app $APP_NAME  --force
if [ $? -eq 0 ]; then
  echo "Frappe app: $APP_NAME uninstall successful"
else
  echo "Frappe app: $APP_NAME uninstall failed"
fi
bench --version
if [ $? -eq 0 ]; then
  echo "Frappe Bench version check successful"
else
  echo "Frappe Bench version check failed. Is it python available or are you running in the correct virtualenv?"
  exit 1
fi
bench --site $SITE clear-cache
bench --site $SITE install-app $APP_NAME
if [ $? -eq 0 ]; then
  echo "Frappe app: $APP_NAME install successful"
else
  echo "Frappe app: $APP_NAME install failed"
fi

echo "Update completed"
