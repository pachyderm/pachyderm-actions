import python_pachyderm
import networkx as nx
from urllib.parse import urlparse
import os
import json

docker_image_name = os.environ["DOCKER_IMAGE_NAME"]
pipeline_files = os.environ["PACHYDERM_PIPELINE_FILES"].split(" ")
git_sha = os.environ["GITHUB_SHA"]


def setup_client():
    pach_url = urlparse(os.environ["PACHYDERM_CLUSTER_URL"])
    pach_token = os.environ["PACHYDERM_TOKEN"]
    host = pach_url.hostname
    port = pach_url.port
    if port is None:
        port = 80
    if pach_url.scheme == "https" or pach_url.scheme == "grpcs":
        tls = True
    else:
        tls = False
    return python_pachyderm.Client(
        host=host, port=port, tls=tls, auth_token=pach_token
    )


def create_pipeline_dict(pipeline_files):
    pipelines = {}
    for pipes in pipeline_files:
        if os.path.isfile(pipes):
            f = open(pipes)
            pipe = json.load(f)
            pipelines[pipe["pipeline"]["name"]] = pipe
        elif os.path.isdir(pipes):
            for dirpath, dirs, files in os.walk(pipes):
                for file in files:
                    f = open(os.path.join(dirpath, file))
                    pipe = json.load(f)
                    pipelines[pipe["pipeline"]["name"]] = pipe
    return pipelines


def get_multi_inputs(pipelinename, input_dict):
    input_list = []
    k = list(input_dict.keys())[0]
    for repo in input_dict[k]:
        if 'pfs' in repo:
            input_list.append((repo["pfs"]["repo"], pipelinename))
        elif any([multi_type in repo for multi_type in ['union', 'cross', 'group', 'join']]):
            return input_list + get_multi_inputs(pipelinename, repo)
    return input_list


def create_connections(pipelines):
    connections = []
    for k, v in pipelines.items():
        output = k
        if "pfs" in v["input"]:
            input = v["input"]["pfs"]["repo"]
            connections.append((input, output))
        elif "cron" in v["input"]:
            # use the name "cron". Really just using this to count in_edges
            connections.append(("cron", output))
        else:
            connections = connections + get_multi_inputs(k, v["input"])
    return connections


def update_image(pipelines, docker, sha):
    updated_pipes = {}
    for k, v in pipelines.items():
        new_pipe = v
        if "image" in new_pipe["transform"]:
            new_pipe["transform"]["image"] = f"{docker}:{sha}"
        updated_pipes[k] = new_pipe
    return updated_pipes


def build_pipeline_dag(pipeline_connections):
    graph = nx.DiGraph()
    graph.add_edges_from(pipeline_connections)
    return graph


def sort_pipelines(graph):
    # Order the nodes topologically, only get nodes that have at least 1 input node (e.g. not a bare repo or cron)
    return [n for n in nx.topological_sort(graph) if len(graph.in_edges(n)) > 0]


def repo_dependencies(graph):
    return [node for node in graph if len(graph.in_edges(node)) == 0 and node != 'cron']


def update_pipeline(pipeline_order, pipelines):
    pipelines_to_update = [i for i in pipeline_order if i in pipelines.keys()]
    client = setup_client()
    for pipe in pipelines_to_update:
        updated_pipe = pipelines[pipe]
        updated_pipe["update"] = True
        req = python_pachyderm.parse_dict_pipeline_spec(updated_pipe)
        client.create_pipeline_from_request(req)


def main():
    pipeline_dict = create_pipeline_dict(pipeline_files)
    updated_pipeline = update_image(pipeline_dict, docker_image_name, git_sha)
    conns = create_connections(updated_pipeline)
    graph = build_pipeline_dag(conns)
    pipeline_order = sort_pipelines(graph)

    # Below gets the repos that this pipeline needs that are not defined in the pipeline list.
    # dependencies = repo_dependencies(graph)

    update_pipeline(pipeline_order, updated_pipeline)


if __name__ == "__main__":
    main()
