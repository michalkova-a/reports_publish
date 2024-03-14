# Reports publish

Utility for creating reports signpost. Can be used to create `index.html` for GitHub pages.

Script runs through given folder and looks for .html files (recursively). Creates simple page where headers correspond to folder structure. Found reports are listed as links to the .html pages.

Usage:
```
python src/reports-publish/html_file_with_links.py docs index.html
```
where `docs` is folder to browse and `index.html` is resulting .html page.
