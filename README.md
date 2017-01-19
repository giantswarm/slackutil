# Slack Mass Join/Leave

To join several Slack channels at once:


```nohighlight
export SLACK_TOKEN=<mytoken>

docker run --rm -ti -e SLACK_TOKEN=${SLACK_TOKEN} giantswarm/slackutil join --include "support-.*" --exclude "support-meta"
```

Leaving several channels at once works the same way, using the `leave` keyword:

```nohighlight
docker run --rm -ti -e SLACK_TOKEN=${SLACK_TOKEN} giantswarm/slackutil leave --include "support-.*" --exclude "support-meta"
```

To just test your include and exclude patterns, use `list` instead:

```nohighlight
docker run --rm -ti -e SLACK_TOKEN=${SLACK_TOKEN} giantswarm/slackutil list --include "a.*" --exclude "abc.*"
```
