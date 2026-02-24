# docs/ — Langflow Documentation Site

## Purpose
Docusaurus-based documentation site for Langflow. Contains all user-facing documentation — getting started guides, component references, tutorials, deployment guides, integration docs, and API reference.

## Folder Structure

| Folder | Description |
|--------|-------------|
| `docs/` | Markdown documentation content organized by topic (Components, Concepts, Configuration, Deployment, etc.). |
| `css/` | Custom CSS styles for the Docusaurus site. |
| `i18n/` | Internationalization — Spanish (es) and French (fr) translations. |
| `research/` | Internal research documents and deep-dive analyses. |
| `src/` | Custom Docusaurus React components and theme overrides. |
| `static/` | Static assets — images, videos, logos, downloadable files. |

## Key Files

| File | Description |
|------|-------------|
| `docusaurus.config.js` | Docusaurus site configuration — navigation, plugins, theme settings. |
| `sidebars.js` | Sidebar navigation structure for the documentation site. |
| `package.json` | Node.js dependencies for the docs site. |
| `openapi.json` | OpenAPI specification for the Langflow API — used for auto-generated API reference docs. |
| `tailwind.config.js` | Tailwind CSS configuration for docs site styling. |

## For LLM Coding Agents
- Documentation is written in Markdown with Docusaurus front matter (title, description, sidebar_position).
- Run `yarn start` from this directory to preview docs locally.
- When adding new backend components, add corresponding documentation in `docs/Components/`.
- When adding new integrations, create a subdirectory in `docs/Integrations/`.
