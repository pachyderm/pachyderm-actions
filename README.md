# Pachyderm GitHub Actions

<p align="center">
	<img src='https://raw.githubusercontent.com/pachyderm/pachyderm/master/doc/docs/master/assets/images/Pachyderm-Character_600.png' height='175' title='Pachyderm'>
</p>

## Pipeline Update Action

Note: The GitHub action updates or creates the pipeline, but does not create or delete versioned data repositories. Any input repositories should already exist or the pipeline cannot be created.

### Usage

To use the Pachyderm action in your workflow, use:

```yaml
- uses: pachyderm/pachyderm-actions/pipeline-action@master
  env:
    PACHYDERM_CLUSTER_URL: ${{ secrets.PACHYDERM_URL }}
    PACHYDERM_TOKEN: ${{ secrets.PACHYDERM_TOKEN }}
    DOCKER_IMAGE_NAME: ${{ secrets.DOCKER_IMAGE }}
    PACHYDERM_PIPELINE_FILES: <list pipeline JSON files to be updated>
```

For more details or customizations of this action, see our [example](https://github.com/pachyderm/pachyderm-gha).

### Configuration

To authorize GitHub Actions to push new information to your cluster you must set up the following secrets:

1. `PACHYDERM_CLUSTER_URL`: This is the url to your pachyderm cluster, the one configured via Ingress to `pachd`'s GRPC port.
    If you use Pachyderm Hub, it'll look something like `grpcs://hub-some-id.clusters.pachyderm.io:31400`.

2. `DOCKER_IMAGE_NAME`: Replace this with the base repo/tag combination for the Docker registry to which your image will be pushed.

3. `PACHYDERM_PIPELINE_FILES`: A space-delimited list of pipeline specifications that depend on `DOCKER_IMAGE_NAME`. It can either be
    specific json files, or folders which contains multiple files.

### Secrets

1. `PACHYDERM_TOKEN`: This is an authentication token to access the Pachyderm cluster. You can generate it using `pachctl auth get-auth-token --ttl <some duration>`. For information on setting the `--ttl` duration, see [generating the Pachyderm authentication token](https://github.com/pachyderm/pachyderm-gha#generating-the-pachyderm-authentication-token) below.

2. `DOCKERHUB_TOKEN` and `DOCKERHUB_USERNAME`: for GitHub to be able to push the Docker image once it is built. For information on creating a Docker Hub token, see [Managing Access Tokens](https://docs.docker.com/docker-hub/access-tokens/).

## Pachctl Command Action

### Usage

To use the `pachctl` action in your workflow, use:

```yaml
- uses: pachyderm/pachyderm-actions/pachctl-action@master
  env:
    PACHYDERM_TOKEN: ${{ secrets.PACHYDERM_TOKEN }}
    PACHYDERM_CLUSTER_URL: ${{ secrets.PACHYDERM_CLUSTER_URL }}
    VERSION: 2.0.5
    COMMAND: "version"
```

### Configuration

To use the action, you need to set the following environment variables:

1. `VERSION`: This is the version of the `pachctl` binary you wish to use. If you do not supply it, we'll use the newest version.
2. `COMMAND`: This is the pachctl command you wish to run. For example to run `pachctl start commit` you would put `start commit` here.

To authorize GitHub Actions to call commands to your cluster you must set up the following secrets:

1. `PACHYDERM_CLUSTER_URL`: This is the url to your pachyderm cluster, the one configured via Ingress to `pachd`'s GRPC port.
    If you use Pachyderm Hub, it'll look something like `grpcs://hub-some-id.clusters.pachyderm.io:31400`.

2. `PACHYDERM_TOKEN`: This is an authentication token to access the Pachyderm cluster. You can generate it using `pachctl auth get-auth-token --ttl <some duration>`. For information on setting the `--ttl` duration, see [generating the Pachyderm authentication token](https://github.com/pachyderm/pachyderm-gha#generating-the-pachyderm-authentication-token) below.

## License

[Pachyderm License](./LICENSE)
