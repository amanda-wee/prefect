from typing import Any

import docker

from prefect import Task
from prefect.utilities.tasks import defaults_from_attrs


class ListImages(Task):
    """
    Task for listing Docker images.
    Note that all initialization arguments can optionally be provided or overwritten at runtime.

    Args:
        - repository_name (str, optional): Only show images belonging to this repository;
            if not provided then it will list all images from the local Docker server
        - all_layers (bool, optional): Show intermediate image layers
        - docker_server_url (str, optional): URL for the Docker server. Defaults to
            `unix:///var/run/docker.sock` however other hosts such as `tcp://0.0.0.0:2375`
            can be provided
    """

    def __init__(
        self,
        repository_name: str = None,
        all_layers: bool = False,
        docker_server_url: str = "unix:///var/run/docker.sock",
        **kwargs: Any
    ):
        self.repository_name = repository_name
        self.all_layers = all_layers
        self.docker_server_url = docker_server_url

        super().__init__(**kwargs)

    @defaults_from_attrs("repository_name", "all_layers", "docker_server_url")
    def run(
        self,
        repository_name: str = None,
        all_layers: bool = False,
        docker_server_url: str = "unix:///var/run/docker.sock",
    ) -> list:
        """
        Task run method.

        Args:
            - repository_name (str, optional): Only show images belonging to this repository;
                if not provided then it will list all images from the local Docker server
            - all_layers (bool, optional): Show intermediate image layers
            - docker_server_url (str, optional): URL for the Docker server. Defaults to
                `unix:///var/run/docker.sock` however other hosts such as `tcp://0.0.0.0:2375`
                can be provided

        Return:
            - list: A list of dictionaries containing information about the images found
        """
        client = docker.APIClient(base_url=docker_server_url)

        return client.images(name=repository_name, all=all_layers)


class PullImage(Task):
    """
    Task for pulling a Docker image.
    Note that all initialization arguments can optionally be provided or overwritten at runtime.

    Args:
        - repository (str, optional): The repository to pull the image from
        - tag (str, optional): The tag of the image to pull; if not specified then the
            `latest` tag will be pulled
        - docker_server_url (str, optional): URL for the Docker server. Defaults to
            `unix:///var/run/docker.sock` however other hosts such as `tcp://0.0.0.0:2375`
            can be provided
    """

    def __init__(
        self,
        repository: str = None,
        tag: str = None,
        docker_server_url: str = "unix:///var/run/docker.sock",
        **kwargs: Any
    ):
        self.repository = repository
        self.tag = tag
        self.docker_server_url = docker_server_url

        super().__init__(**kwargs)

    @defaults_from_attrs("repository", "tag", "docker_server_url")
    def run(
        self,
        repository: str = None,
        tag: str = None,
        docker_server_url: str = "unix:///var/run/docker.sock",
    ) -> str:
        """
        Task run method.

        Args:
            - repository (str, optional): The repository to pull the image from
            - tag (str, optional): The tag of the image to pull; if not specified then the
                `latest` tag will be pulled
            - docker_server_url (str, optional): URL for the Docker server. Defaults to
                `unix:///var/run/docker.sock` however other hosts such as `tcp://0.0.0.0:2375`
                can be provided

        Return:
            - str: The output from Docker for pulling the image

        Raises:
            - ValueError: if `repository` is `None`
        """
        if not repository:
            raise ValueError("A repository to pull the image from must be specified.")

        client = docker.APIClient(base_url=docker_server_url)

        return client.pull(repository=repository, tag=tag)


class PushImage(Task):
    """
    Task for pushing a Docker image.
    Note that all initialization arguments can optionally be provided or overwritten at runtime.

    Args:
        - repository (str, optional): The repository to push the image to
        - tag (str, optional): The tag for the image to push; if not specified then the
            `latest` tag will be pushed
        - docker_server_url (str, optional): URL for the Docker server. Defaults to
            `unix:///var/run/docker.sock` however other hosts such as `tcp://0.0.0.0:2375`
            can be provided
    """

    def __init__(
        self,
        repository: str = None,
        tag: str = None,
        docker_server_url: str = "unix:///var/run/docker.sock",
        **kwargs: Any
    ):
        self.repository = repository
        self.tag = tag
        self.docker_server_url = docker_server_url

        super().__init__(**kwargs)

    @defaults_from_attrs("repository", "tag", "docker_server_url")
    def run(
        self,
        repository: str = None,
        tag: str = None,
        docker_server_url: str = "unix:///var/run/docker.sock",
    ) -> str:
        """
        Task run method.

        Args:
            - repository (str, optional): The repository to push the image to
            - tag (str, optional): The tag for the image to push; if not specified then the
                `latest` tag will be pushed
            - docker_server_url (str, optional): URL for the Docker server. Defaults to
                `unix:///var/run/docker.sock` however other hosts such as `tcp://0.0.0.0:2375`
                can be provided

        Return:
            - str: The output from Docker for pushing the image

        Raises:
            - ValueError: if `repository` is `None`
        """
        if not repository:
            raise ValueError("A repository to push the image to must be specified.")

        client = docker.APIClient(base_url=docker_server_url)

        return client.push(repository=repository, tag=tag)


class RemoveImage(Task):
    """
    Task for removing a Docker image.
    Note that all initialization arguments can optionally be provided or overwritten at runtime.

    Args:
        - image (str, optional): The image to remove
        - force (bool, optional): Force removal of the image
        - docker_server_url (str, optional): URL for the Docker server. Defaults to
            `unix:///var/run/docker.sock` however other hosts such as `tcp://0.0.0.0:2375`
            can be provided
    """

    def __init__(
        self,
        image: str = None,
        force: bool = False,
        docker_server_url: str = "unix:///var/run/docker.sock",
        **kwargs: Any
    ):
        self.image = image
        self.force = force
        self.docker_server_url = docker_server_url

        super().__init__(**kwargs)

    @defaults_from_attrs("image", "force", "docker_server_url")
    def run(
        self,
        image: str = None,
        force: bool = False,
        docker_server_url: str = "unix:///var/run/docker.sock",
    ) -> None:
        """
        Task run method.

        Args:
            - image (str, optional): The image to remove
            - force (bool, optional): Force removal of the image
            - docker_server_url (str, optional): URL for the Docker server. Defaults to
                `unix:///var/run/docker.sock` however other hosts such as `tcp://0.0.0.0:2375`
                can be provided

        Raises:
            - ValueError: if `image` is `None`
        """
        if not image:
            raise ValueError("The name of an image to remove must be provided.")

        client = docker.APIClient(base_url=docker_server_url)

        client.remove(image=image, force=force)


class TagImage(Task):
    """
    Task for tagging a Docker image.
    Note that all initialization arguments can optionally be provided or overwritten at runtime.

    Args:
        - image (str, optional): The image to tag
        - repository (str, optional): The repository to set for the tag
        - tag (str, optional): The tag name for the image
        - force (bool, optional): Force tagging of the image
        - docker_server_url (str, optional): URL for the Docker server. Defaults to
            `unix:///var/run/docker.sock` however other hosts such as `tcp://0.0.0.0:2375`
            can be provided
    """

    def __init__(
        self,
        image: str = None,
        repository: str = None,
        tag: str = None,
        force: bool = False,
        docker_server_url: str = "unix:///var/run/docker.sock",
        **kwargs: Any
    ):
        self.image = image
        self.repository = repository
        self.tag = tag
        self.force = force
        self.docker_server_url = docker_server_url

        super().__init__(**kwargs)

    @defaults_from_attrs("image", "repository", "tag", "force", "docker_server_url")
    def run(
        self,
        image: str = None,
        repository: str = None,
        tag: str = None,
        force: bool = False,
        docker_server_url: str = "unix:///var/run/docker.sock",
    ) -> None:
        """
        Task run method.

        Args:
            - image (str, optional): The image to tag
            - repository (str, optional): The repository to set for the tag
            - tag (str, optional): The tag name for the image
            - force (bool, optional): Force tagging of the image
            - docker_server_url (str, optional): URL for the Docker server. Defaults to
                `unix:///var/run/docker.sock` however other hosts such as `tcp://0.0.0.0:2375`
                can be provided

        Return:
            - bool: Whether or not the tagging was successful

        Raises:
            - ValueError: if either `image` or `repository` are `None`
        """
        if not image or not repository:
            raise ValueError("Both image and repository must be provided.")

        client = docker.APIClient(base_url=docker_server_url)

        return client.tag(image=image, repository=repository, tag=tag, force=force)
