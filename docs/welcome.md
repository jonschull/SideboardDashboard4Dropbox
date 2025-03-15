## Welcome to SideBarDashboard4Dropbox!

This is a simple, clean static dashboard with markdown sidebar that allows you to:

#### 1. View content in properly positioned windows
- Markdown files (`.md`) are rendered automatically with proper formatting
- External links open in new windows
- The sidebar is fixed at 300px width

#### 2. Edit local content with a text editor and see  live previews in the browser when you 
* You can edit .md and .html files yourself using any text edtior.
* but with [Windsurf](https://codeium.com/windsurf/download) you also get AI assistance authoring and researching
        * once you've downloaded Windsurf, you can double click the file called 
        `DoubleClick_if_you_have_Windsurf.code-workspace`

## Advice

### Advice for Author/Editors

All content is served from the `docs` directory:

- `docs/sidebar.md` - The main navigation sidebar content.  _You can edit this._
- `docs/js/viewer.js` - The JavaScript that powers the dashboard.  _Do not edit_
- `docs/css/styles.css` - The styling for the dashboard _do not edit_
- `docs` is for markdown and html files you edit and create.

### Adding Content

1. Create new markdown (`.md`) or HTML (`.html`) files in the `docs` directory
2. Add links to these files in `sidebar.md`
3. The sidebar will automatically refresh when you update `sidebar.md`

Example sidebar entry:

```markdown
- [My New Page](my-new-page.md)
```

## Using with Windsurf AI Assistant

If you're running this dashboard in the Windsurf app, you can leverage the AI assistant to help you:

Simply ask the AI assistantin natural language, for example:

- "Create a new page about [topic]"
- "Help me format this markdown file"
