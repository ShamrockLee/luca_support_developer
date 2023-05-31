from typing import List, Optional
import json
import os
from .utils import is_directly_imported_in_jupyter_notebook



def support_message(
    package_name: str,
    developer_name: str,
    github_handle: str,
    image_url: str,
    repository_name: Optional[str] = None,
    number_of_imports: List[int] = (5, 100, 1000, 5000),
    always_show: bool = False,
    config_dir: str = os.path.expanduser("~/.config/support_developer"),
    config_filename: str = "import_count.json",
):
    """Displays a banner asking user to support developer.

    Parameters
    --------------
    package_name: str
        Name of the package to ask support for.
    developer_name: str
        Name of the developer to display.
    github_handle: str
        GitHub handle of the developer.
    repository_name: Optional[str] = None
        Repository GitHub to link.
    image_url: str
        Link to an image of interest to display.
    number_of_imports: List[int] = (5, 100, 1000)
        Import cases where we should display this banner.
    always_show: bool = False
        Whether to always display the message.
    config_dir: str = "~/.config/support_developer"
        The configuration directory
        This could be the config directory of the main package if it uses one.
    config_filename: str = "import_count.json"
        The name of the configuration file to record the number of imports.
    """
    if repository_name is None:
        repository_name = package_name

    if not is_directly_imported_in_jupyter_notebook():
        return

    from IPython.display import HTML, display

    # Path where to store the loading counts
    path = os.path.join(config_dir, config_filename)

    # Ensure the configuration directory is writable
    config_dir_real: str = os.path.realpath(config_dir)
    is_dir_writable: bool = True
    if os.path.isdir(config_dir_real):
        if not os.access(config_dir, os.W_OK) or not os.access(config_dir_real, os.W_OK):
            is_dir_writable = False
    elif os.path.exists(config_dir):
        is_dir_writable = False
    else:
        try:
            os.makedirs(config_dir)
        except OSError:
            is_dir_writable = False

    if not always_show and not is_dir_writable:
        return

    # Ensure the configuration file is writable, and
    # Check how many times this package was already
    # imported by this user.

    config_file_real = os.path.realpath(path)
    is_file_writable: bool = True
    if os.path.exists(config_file_real):
        if (os.path.isdir(config_file_real)
        or not os.access(path, os.W_OK)
        or not os.access(config_file_real, os.W_OK)):
            is_file_writable = False
            if not always_show:
                return
        else:
            with open(path, "r") as f:
                metadata = json.load(f)
    else:
        metadata = dict()

    if is_file_writable:
        metadata[package_name] = metadata.get(package_name, 0) + 1
        with open(path, "w") as f:
            json.dump(metadata, f)

    # If this is not one of those import cases where we expect
    # to show this banner, we skip forward.
    if not always_show and metadata[package_name] not in number_of_imports:
        return

    if metadata[package_name] > number_of_imports[0]:
        long_time_user_message = """
        <span>I hope my work has saved you some time!</span><br/>
        """
    else:
        long_time_user_message=""

    display(HTML(
        """
        <style>
            .support_message_main_box {{
                position: relative;
                display: table-cell;
                vertical-align: middle;
                width: 100%;
                height: 8em;
                padding: 1em;
                padding-left: 11em;
                background-color: #f7f7f7;
                border: 1px solid #cfcfcf;
                border-radius: 2px;
            }}
            .support_message_main_box img {{
                position: absolute;
                height: 9em;
                width: 9em;
                left: 0.5em;
                top: 0.5em;
                border-radius: 1em;
            }}
        </style>
        <div class="support_message_main_box">
            <img src="{image_url}" />
            <p>
            <b>Hi!</b><br/>
            <span>I am the author of
            <a href="https://github.com/{github_handle}/{repository_name}" target="_blank">
                {package_name}
            </a>, which you use in this Notebook.
            </span><br/>
            {long_time_user}
            <span>I love to code, but I also need coffee.</span>
            <a href="https://github.com/sponsors/{github_handle}" target="_blank">
                Please sponsor me on GitHub ❤️
            </a><br/>
            <i>Good luck in your coding 🍀!</i>
            <br/>
            <i>- {developer_name}</i>
            </p>
        <div>
        """.format(
            developer_name=developer_name,
            package_name=package_name,
            repository_name=repository_name,
            image_url=image_url,
            long_time_user=long_time_user_message,
            github_handle=github_handle
        )
    ))