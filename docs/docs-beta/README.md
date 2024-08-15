# Dagster Docs - Beta

This is the home of the new Dagster documentation. It is currently in beta and incomplete.
The documentation site is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

---

## Installation

The site uses [yarn](https://yarnpkg.com/) for package management. 

To install dependencies: 

```
yarn install
```

**Note**: The yarn binary is checked in, so you do not need to install yarn yourself.

It also uses [Vale](https://vale.sh/) to check for issues in the documentation.

Install Vale with:

```bash
brew install vale
```

---

## Overview of the docs

- `./src` contains custom components, styles, themes, and layouts.
- `./content-templates` contains the templates for the documentation pages.
- `./docs/` is the source of truth for the documentation.
- `./docs/code_examples` contains all code examples for the documentation.

The docs are broken down into the following sections:

- [Tutorials](./docs/tutorials/)
- [Guides](./docs/guides/)
- [Concepts](./docs/concepts/)

`sidebar.ts` and `docusaurus.config.ts` are the main configuration files for the documentation.

---

## Local Development

To start the local development server:

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server. Access the website at [http://localhost:3050](http://localhost:3050).

To check the documentation for different issues, use the following:

```bash
## Lints Markdown content using prettier
yarn lint

## Lints documentation content using Vale Server
## Checks for style guide adherence, grammar, spelling, etc.
yarn lint:vale

## Autofixes issues caught by prettier
yarn lint:fix
```

---

## Build

To build the site for production:

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.