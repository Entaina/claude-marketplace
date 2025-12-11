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

<!-- Plugins will be listed here as they are added -->

*No plugins available yet. See "Creating Plugins" below to add your first plugin.*

## Creating Plugins

### Option 1: Add a plugin from this repository

1. Create your plugin in the `plugins/` directory:

```
plugins/
  my-plugin/
    .claude-plugin/
      plugin.json
    .claude/
      commands/
        my-command.md
      skills/
        my-skill/
          SKILL.md
      agents/
        my-agent.md
```

2. Add it to `.claude-plugin/marketplace.json`:

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin",
  "description": "Description of what the plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  },
  "keywords": ["keyword1", "keyword2"],
  "category": "productivity"
}
```

### Option 2: Reference an external GitHub repository

```json
{
  "name": "external-plugin",
  "source": {
    "source": "github",
    "repo": "username/plugin-repo"
  },
  "description": "An external plugin"
}
```

### Option 3: Reference any git repository

```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

## Plugin Entry Schema

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Plugin identifier (kebab-case) |
| `source` | Yes | Path or source object |
| `description` | No | Brief description |
| `version` | No | Semantic version |
| `author` | No | Author info object |
| `homepage` | No | Documentation URL |
| `repository` | No | Source code URL |
| `license` | No | SPDX license (MIT, Apache-2.0, etc.) |
| `keywords` | No | Discovery tags |
| `category` | No | Plugin category |
| `strict` | No | Require plugin.json (default: true) |

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
