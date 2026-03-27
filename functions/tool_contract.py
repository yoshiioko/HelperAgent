from abc import ABC, abstractmethod

class ToolContract(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """A unique name for the tool."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """A short description of what the tool does."""
        pass

    @abstractmethod
    def run(self, working_directory: str, **kwargs):
        """Execute the tool's main logic."""
        pass

