[![](https://img.shields.io/docker/automated/giantswarm/slackutil.svg)](https://hub.docker.com/r/giantswarm/slackutil/)

# Slack Mass Join/Leave

## Usage

Before you can start, set up the `SLACK_TOKEN` environment variable with a valid [Slack token](https://api.slack.com/docs/oauth-test-tokens) as value and create an alias `slackutil` as you can see below:

```nohighlight
export SLACK_TOKEN=<mytoken>
```

Create a `slackutil` alias for your convenience:

```nohighlight
alias slackutil="docker run --rm -ti -e SLACK_TOKEN=${SLACK_TOKEN} giantswarm/slackutil"
```

General command syntax:

```nohighlight
slackutil <join|leave|list> [--include <include-pattern> [--exclude <exclude-pattern>]]
```

### Joining channels

To join all channels available to you:

```nohighlight
slackutil join
```

To join all channels with names starting with `ux-`:

```nohighlight
slackutil join --include "ux-.*"
```

To join all channels with names matching `ux-.*`, but not matching `ux-noise`:

```nohighlight
slackutil join --include "ux-.*" --exclude "ux-noise"
```

You can use as many `--include` and `--exclude` patterns as you want to.

Pro tip: **Test your patterns** as described below before actually joining channels.

### Leaving channels

The `leave` command works the same way as the `join` command.

To leave all channels containing `jokes` in their name, except for the one named `actually-funny-jokes`:

```nohighlight
slackutil leave --include ".*jokes.*" --exclude "actually-funny-jokes"
```

### Testing your patterns

To just test your include and exclude patterns, use `list` instead:

```nohighlight
slackutil list --include "a.*" --exclude "abc.*"
```

This way, the matching channel names will be printed. Nothing else.
