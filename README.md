# Entaina Claude Code Marketplace

A curated collection of Claude Code plugins for AI-powered development workflows.

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add entaina/claude-marketplace
```

Or for local development:

```bash
/plugin marketplace add /path/to/claude-marketplace
```

## Browse & Install Plugins

After adding the marketplace:

```bash
# Interactive plugin browser
/plugin

# Install a specific plugin
/plugin install plugin-name@entaina
```

## Available Plugins

| Plugin | Description | Category |
|--------|-------------|----------|
| [vcs](plugins/vcs) | Spanish-language version control commands for non-technical users. Simplifies Git operations with natural language file selection and auto-generated commit messages. | devops |
| [product-dev](plugins/product-dev) | Gestión del ciclo de vida de features: crear, documentar con PRD, dividir en tareas, planificar e implementar. | workflow |
| [visual-explainer](https://github.com/Entaina/visual-explainer) | Explicaciones visuales como páginas HTML autocontenidas o decks Slidev: diagramas, arquitecturas, reviews de diff y de plan, recaps, tablas comparativas, slides y fact-check. | documentation |
| [skiller](https://github.com/Entaina/skiller) | Define, crea, extrae, valida y publica Agent Skills, distribuibles con skills.sh y versionadas con release-please. | productivity |
| [git-skill](https://github.com/Entaina/git-skill) | Convenciones Git y mensajes de commit siguiendo estrictamente Conventional Commits v1.0.0. | devops |

## Adding a plugin

1. **One repository per plugin.** This repository only lists plugins; it
   doesn't host them. (`vcs` and `product-dev` still live here for now.)
2. **Skills follow [Agent Skills](https://agentskills.io/specification).**
   Each one lives in `skills/<name>/SKILL.md`, and its frontmatter `name`
   matches the directory.
3. **Standards first, extras opt-in.** A root `plugin.json` following
   [Agent Plugins](https://agent-plugins.org) is optional; when present, its
   `name` matches the catalogue entry. Client-specific extras
   (`.claude-plugin/plugin.json`, `dependencies`, agents) are allowed, but the
   plugin must work without them. Claude Code reads the root `plugin.json`
   unless `.claude-plugin/plugin.json` exists, and never merges the two.
4. **Names describe the scope, not the tool.** Kebab-case, no `-skill` or
   `-plugin` suffix, and the repository is named after the plugin.
5. **Register the plugin in both catalogues** with the smallest entry that
   works, and no `version` (it comes from the plugin itself):

   - `.claude-plugin/marketplace.json` (Claude Code):
     ```json
     { "name": "my-plugin",
       "source": { "source": "github", "repo": "Entaina/my-plugin" },
       "description": "…", "category": "productivity" }
     ```
     Add `"strict": false` only if the plugin has no manifest of its own.
   - `.agents/plugins/marketplace.json` (Codex and ChatGPT):
     ```json
     { "name": "my-plugin",
       "source": { "source": "url", "url": "https://github.com/Entaina/my-plugin.git" },
       "policy": { "installation": "AVAILABLE", "authentication": "ON_USE" },
       "category": "Productivity" }
     ```
     Use `url`: Codex rejects `github`, `git` and `git-subdir` for a plugin
     at the root of its repository.
6. **Install the plugin from both catalogues before merging**, and check
   that its skills appear.

For every entry field, see the
[Claude Code marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference).

## Plugin Categories

- `productivity` - Workflow automation and efficiency
- `devops` - CI/CD, deployment, infrastructure
- `testing` - Test generation and validation
- `documentation` - Docs generation and maintenance
- `security` - Security scanning and best practices
- `frameworks` - Framework-specific tools

## Marketplace Commands

```bash
# List known marketplaces
/plugin marketplace list

# Update marketplace metadata
/plugin marketplace update entaina

# Remove marketplace
/plugin marketplace remove entaina

# Validate marketplace
claude plugin validate .
```

## Team Distribution

To auto-install this marketplace for your team, add to `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "entaina": {
      "source": {
        "source": "github",
        "repo": "entaina/claude-marketplace"
      }
    }
  }
}
```

## License

MIT
