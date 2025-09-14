FILE=erpnext_engineering/__init__.py
echo "Tagging the repository with the current version from $FILE"
echo "Searching file $FILE for version..."
if [ ! -f $FILE ]; then
  echo "Error: $FILE file not found!"
  exit 1
fi
VERSION=$(grep '__version__' $FILE | cut -d'"' -f2)
echo "Current version is $VERSION"
echo "Creating git tag v$VERSION and pushing to origin"
git tag "v$VERSION"
echo "Pushing tag v$VERSION to origin"
git push origin "v$VERSION"
echo "Tagging completed."