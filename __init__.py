import httpx
import warnings
import toml
from .src import *

from importlib_metadata import version as get_version

project_info = toml.loads(httpx.get("https://raw.githubusercontent.com/Darkstepan/avio/master/pyproject.toml").text)
origin_version = project_info["project"]["version"]
local_version = get_version("avio")

if local_version != origin_version:
    warnings.warn(f"""Possibly outdated version - LOCAL={local_version} != ORIGIN={origin_version} 
    Your version does not match the GitHub version and may be outdated, consider updating with 'pip install --upgrade git+https://github.com/Darkstepan/avio.git'""")
