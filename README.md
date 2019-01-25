[![Docker Repository on Quay](https://quay.io/repository/giantswarm/slackutil/status "Docker Repository on Quay")](https://quay.io/repository/giantswarm/slackutil)

# Slack Mass Join/Leave/Star/Mute tool

This little CLI helps you to join, leave, add/remove stars from/to a bunch of channels based on regex patterns.

## Usage

Before you can start, set up the `SLACK_TOKEN` environment variable with a valid [Slack token](https://api.slack.com/docs/oauth-test-tokens) as value and create an alias `slackutil` as you can see below:

```nohighlight
export SLACK_TOKEN=<mytoken>
alias slackutil="docker run --rm -ti -e SLACK_TOKEN=${SLACK_TOKEN} giantswarm/slackutil"
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

### Adding stars to/from channels

```nohighlight
slackutil star --include "cool-.*"
```

```nohighlight
slackutil unstar --include "uncool-.*"
```

### Muting/unmuting channels

To mute all support channels:

```nohighlight
slackutil mute --include "support-.*"
```

To unmute all support channels:

```nohighlight
slackutil unmute --include "support-.*"
```


### Testing your patterns

To just test your include and exclude patterns, use `list` instead:

```nohighlight
slackutil list --include "a.*" --exclude "abc.*"
```

This way, the matching channel names will be printed. Nothing else.
