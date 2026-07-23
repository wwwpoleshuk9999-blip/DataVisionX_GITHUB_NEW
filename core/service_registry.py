from typing import Any, Dict


class ServiceRegistry:
    """
    Central registry for DataVisionX platform services.

    Responsible for:
    - registering services
    - retrieving services
    - checking availability
    - removing services
    """

    def __init__(self):
        self._services: Dict[str, Any] = {}


    def register(self, name: str, service: Any):
        """
        Register a service.
        """

        if not name:
            raise ValueError("Service name is required")

        if name in self._services:
            raise ValueError(
                f"Service already registered: {name}"
            )

        self._services[name] = service


    def get(self, name: str):
        """
        Get service instance.
        """

        return self._services.get(name)


    def require(self, name: str):
        """
        Get service or raise error.
        """

        service = self.get(name)

        if service is None:
            raise RuntimeError(
                f"Service not found: {name}"
            )

        return service


    def exists(self, name: str) -> bool:
        """
        Check service existence.
        """

        return name in self._services


    def unregister(self, name: str):
        """
        Remove service.
        """

        if name in self._services:
            del self._services[name]


    def list_services(self):
        """
        Return registered service names.
        """

        return list(
            self._services.keys()
        )


    def clear(self):
        """
        Remove all services.
        """

        self._services.clear()


service_registry = ServiceRegistry()
