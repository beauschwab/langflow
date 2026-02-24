# icons/ — Custom SVG Icon Components

## Purpose
Contains custom SVG icon components for third-party service logos and branded icons used throughout the Langflow UI. Each subdirectory holds an SVG asset and a React component wrapper for one brand/service icon.

## Structure
Each icon subdirectory follows the same pattern:
- An `.svg` file with the icon artwork
- A `.jsx` or `.tsx` React component that renders the SVG
- An `index.tsx` barrel export

## Usage
Icons are imported by the `genericIconComponent` and `renderIconComponent` in `components/common/` and rendered in component nodes, sidebar entries, and other UI locations based on the component's `icon` field from the backend.

## For LLM Coding Agents
- To add a new icon: create a subdirectory here with the SVG file and a React wrapper component.
- Icon names should match the backend component's `icon` field value.
- The parent `icons/` directory has a lazy-loading index that maps icon names to components.
