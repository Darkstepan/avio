# AVio
## About

A dataclass based Vio API wrapper for Python. Supports both synchronous and asynchronous interface.

## Instalation

The recommended way is to download the package from GitHub directly with pip:

`pip install git+https://github.com/Darkstepan/avio.git`

## Example Usage
```python
from avio import Client

client = Client("YOUR-API-KEY")
scan = client.get_current_scan()
print(scan.scan_id)
```

## Help

If you run into trouble when using this package, you can [open an issue](https://github.com/Darkstepan/avio/issues/new) or contact me directly on discord.

