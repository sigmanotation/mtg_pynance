from pathlib import Path


class Config:
    """
    Class defining the configuration to run mtg_pynance with.

    Parameters
    ----------
    workspace_path: Path
        Path to the workspace directory.
    collection_path: Path
        Path to the card collection csv file.

    Methods
    -------
    create_workspace()
        Creates the workspace folder.
    get_bulk_info_path() -> Path
        Returns the path of Scryfall's bulk data default cards information
        json file.
    get_bulk_data_path() -> Path
        Returns the path of Scryfall's bulk data default cards json file.
    """

    def __init__(self, workspace_path: Path, collection_path: Path) -> None:
        self.workspace_path = workspace_path
        self.collection_path = collection_path

    def create_workspace(self):
        """
        Creates the workspace folder.
        """
        if not self.workspace_path.exists():
            self.workspace_path.mkdir()

    def get_bulk_info_path(self) -> Path:
        """
        Returns the path of Scryfall's bulk data default cards information
        json file.
        """
        path = self.workspace_path / "bulk_default_info.json"
        return path

    def get_bulk_data_path(self) -> Path:
        """
        Returns the path of Scryfall's bulk data default cards json file.
        """
        path = self.workspace_path / "bulk_default_data.json"
        return path
