"""Python wrapper & utilities for Rust communications engine.
"""

from .rpc import *
from .show import *
from ._result import Result, set_error_hook
from . import _result as result
from ._option import Option as Option
from . import _option as option
