"""
Abstract class definitions for containers.
"""
from __future__ import print_function, unicode_literals

from conu.apidefs.image import Image

import requests
from six.moves.urllib.parse import urlunsplit


class Container(object):
    """
    Container class definition which contains abstract methods. The instances should call the
    constructor
    """
    def __init__(self, image, container_id, name):
        """
        :param image: Image instance
        :param container_id: str, unique identifier of this container
        :param container_id: str, pretty container name
        """
        if not isinstance(image, Image):
            raise RuntimeError("image argument is not an instance of Image class")
        self.image = image
        self._id = container_id
        self._metadata = None
        self.name = name
        # provides HTTP client (requests.Session)
        self.http_session = requests.Session()

    def http_request(self, path="/", method="GET", host=None, port=None, json=False, data=None):
        """
        perform a HTTP request

        :param path: str, path within the reqest, e.g. "/api/version"
        :param method: str, HTTP method
        :param host: str, if None, set self.get_IPv4s()[0]
        :param port: str, if None, set to self.get_ports()[0]
        :param json: bool, should we expect json?
        :param data: data to send (can be dict, list, str)
        :return: dict
        """
        host = host or self.get_IPv4s()[0]
        port = port or self.get_ports()[0]
        url = urlunsplit(
            ("http", host + ":" + port, path, "", "")
        )
        return self.http_session.request(method, url, json=json, data=data)

    def get_id(self):
        """
        get unique identifier of this container

        :return: str
        """
        raise NotImplementedError("get_id method is not implemented")

    def get_metadata(self, refresh=False):
        """
        return cached metadata by default

        :param refresh: bool, returns up to date metadata if set to True
        :return: dict
        """
        raise NotImplementedError("get_metadata method is not implemented")

    def is_running(self):
        """
        returns True if the container is running, this method should always ask the API and
        should not use a cached value

        :return: bool
        """
        raise NotImplementedError("is_running method is not implemented")

    def status(self):
        """
        Provide current, up-to-date status of this container. This method should not use cached
        value. Implementation of this method should clearly state list of possible values
        to get from this method

        :return: str
        """
        raise NotImplementedError("status method is not implemented")

    def get_pid(self):
        """
        get process identifier of the root process in the container

        :return: int
        """
        raise NotImplementedError("get_pid method is not implemented")

    def name(self):
        """
        Return name of this container.

        :return: str
        """
        raise NotImplementedError("name method is not implemented")

    def get_IPv4s(self):
        """
        Return all knwon IPv4 addresses of this container. It may be possible
        that the container has disabled networking: in that case, the list is
        empty

        :return: list of str
        """
        raise NotImplementedError("get_IPv4s method is not implemented")

    def get_IPv6s(self):
        """
        Return all knwon IPv6 addresses of this container. It may be possible
        that the container has disabled networking: in that case, the list is
        empty

        :return: list of str
        """
        raise NotImplementedError("get_IPv6s method is not implemented")

    def get_ports(self):
        """
        get ports specified in container metadata

        :return: list of str
        """
        raise NotImplementedError("get_ports method is not implemented")

    def is_port_open(self, port, timeout=2):
        """
        check if given port is open and receiving connections

        :param port: int
        :param timeout: int, how many seconds to wait for connection; defaults to 2
        :return: True if the connection has been established inside timeout, False otherwise
        """
        raise NotImplementedError("is_port_open method is not implemented")

    def open_connection(self, port=None):
        """
        open a TCP connection to service running in the container, if port is None and
        container exposes only a single port, connect to it, otherwise raise an exception

        :param port: int or None
        :return: list of int
        """
        raise NotImplementedError("open_connection method is not implemented")

    @classmethod
    def run_via_binary(cls, image, *args, **kwargs):
        """
        create container using provided image and run it in the background; this method is useful
        to test real user scenarios when users invoke containers using binary and not an API

        :param image: instance of Image
        :return: instance of Container
        """
        raise NotImplementedError("run_via_binary method is not implemented")

    @classmethod
    def run_via_api(cls, image, container_params):
        """
        create container using provided image and run it in the background

        :param image: instance of Image
        :param container_params: instance of ContainerParameters
        :return: instance of Container
        """
        raise NotImplementedError("run_via_api method is not implemented")

    @classmethod
    def create(cls, image, container_params):
        """
        create container using provided image

        :param image: instance of Image
        :param container_params: instance of ContainerParameters
        :return: instance of Container
        """
        raise NotImplementedError("create method is not implemented")

    def start(self):
        """
        start current container

        :return: None
        """
        raise NotImplementedError("start method is not implemented")

    # exec is a keyword in python
    def execute(self, command, **kwargs):
        """
        execute a command in this container -- usually the container needs to be running

        TODO: what about parameters?

        :param command: str, command to execute in the container
        :param kwargs:
        :return: ? we need to provide output, exit code and there needs to be a possibility for
                  this thing to be async and blocking
        """
        raise NotImplementedError("execute method is not implemented")

    def logs(self, follow=False):
        """
        get logs from this container

        :param follow: bool, provide iterator if True
        :return: str or iterator
        """
        raise NotImplementedError("logs method is not implemented")

    def stop(self):
        """
        stop this container

        :return: None
        """
        raise NotImplementedError("stop method is not implemented")

    def kill(self, signal=None):
        """
        kill this container

        :param signal: str, signal to use for killing the container
        :return: None
        """
        raise NotImplementedError("kill method is not implemented")

    def rm(self, force=False, **kwargs):
        """
        remove this container; kwargs indicate that some container runtimes
        might accept more parameters

        :param force: bool, if container engine supports this, force the functionality
        :return: None
        """
        raise NotImplementedError("rm method is not implemented")

    def mount(self, mount_point=None):
        """
        mount container filesystem

        :param mount_point: str, directory where the filesystem will be mounted
        :return: instance of Filesystem
        """
        raise NotImplementedError("mount is not implemented")
