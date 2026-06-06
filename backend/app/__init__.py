from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


_factory_path = Path(__file__).resolve().parent.parent / "app.py"
_factory_spec = spec_from_file_location("gth_app_factory", _factory_path)
_factory_module = module_from_spec(_factory_spec)
_factory_spec.loader.exec_module(_factory_module)

create_app = _factory_module.create_app

__all__ = ["create_app"]
