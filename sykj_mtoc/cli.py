"""CLI for sykj_mtoc.

Example usage:
    $ sykj_mtoc <path_to_file> --language java --class_name MyModel --package_name foo.bar.baz
    $ sykj_mtoc --language java < <path_to_file>

Model can also be piped:
    # cat <path_to_file> | sykj_mtoc --language java
"""
import sys
from argparse import ArgumentParser, FileType
from inspect import signature

import numpy as np

import sykj_mtoc

LANGUAGE_TO_EXPORTER = {
    "python": (sykj_mtoc.export_to_python, ["indent", "function_name"]),
    "java": (sykj_mtoc.export_to_java, ["indent", "class_name", "package_name", "function_name"]),
    "c": (sykj_mtoc.export_to_c, ["indent", "function_name"]),
    "go": (sykj_mtoc.export_to_go, ["indent", "function_name"]),
    "javascript": (sykj_mtoc.export_to_javascript, ["indent", "function_name"]),
    "visual_basic": (sykj_mtoc.export_to_visual_basic, ["module_name", "indent", "function_name"]),
    "c_sharp": (sykj_mtoc.export_to_c_sharp, ["indent", "class_name", "namespace", "function_name"]),
    "powershell": (sykj_mtoc.export_to_powershell, ["indent", "function_name"]),
    "r": (sykj_mtoc.export_to_r, ["indent", "function_name"]),
    "php": (sykj_mtoc.export_to_php, ["indent", "function_name"]),
    "dart": (sykj_mtoc.export_to_dart, ["indent", "function_name"]),
    "haskell": (sykj_mtoc.export_to_haskell, ["module_name", "indent", "function_name"]),
    "ruby": (sykj_mtoc.export_to_ruby, ["indent", "function_name"]),
    "f_sharp": (sykj_mtoc.export_to_f_sharp, ["indent", "function_name"]),
    "rust": (sykj_mtoc.export_to_rust, ["indent", "function_name"]),
    "elixir": (sykj_mtoc.export_to_elixir, ["module_name", "indent", "function_name"]),
}


# The maximum recursion depth is represented by the maximum int32 value.
MAX_RECURSION_DEPTH = np.iinfo(np.intc).max


parser = ArgumentParser(
    prog="sykj_mtoc",
    description="Generate code in native language for provided model.")
parser.add_argument(
    "infile",
    type=FileType("rb"),
    nargs="?",
    default=sys.stdin.buffer,
    help="File with pickle representation of the model.")
parser.add_argument(
    "--language", "-l",
    type=str,
    choices=LANGUAGE_TO_EXPORTER.keys(),
    help="Target language.",
    required=True)
parser.add_argument(
    "--function_name", "-fn",
    dest="function_name",
    type=str,
    # The default value is conditional and will be set in the argument's
    # post-processing, based on the signature of the `export` function
    # that belongs to the specified target language.
    default=None,
    help="Name of the function in the generated code.")
parser.add_argument(
    "--class_name", "-cn",
    dest="class_name",
    type=str,
    help="Name of the generated class (if supported by target language).")
parser.add_argument(
    "--package_name", "-pn",
    dest="package_name",
    type=str,
    help="Package name for the generated code (if supported by target language).")
parser.add_argument(
    "--module_name", "-mn",
    dest="module_name",
    type=str,
    help="Module name for the generated code (if supported by target language).")
parser.add_argument(
    "--namespace", "-ns",
    dest="namespace",
    type=str,
    help="Namespace for the generated code (if supported by target language).")
parser.add_argument(
    "--indent", "-i",
    dest="indent",
    type=int,
    default=4,
    help="Indentation for the generated code.")
parser.add_argument(
    "--recursion-limit", "-rl",
    type=int,
    help="Sets the maximum depth of the Python interpreter stack. No limit by default",
    default=MAX_RECURSION_DEPTH)
parser.add_argument(
    "--version", "-v",
    action="version",
    version=f"%(prog)s {sykj_mtoc.__version__}")
parser.add_argument(
    "--pickle-lib", "-pl",
    type=str,
    dest="lib",
    help="Sets the lib used to save the model",
    choices=["pickle", "joblib"],
    default="pickle")


def parse_args(args):
    return parser.parse_args(args)


def generate_code(args):
    sys.setrecursionlimit(args.recursion_limit)

    with args.infile as f:
        pickle_lib = __import__(args.lib)
        model = pickle_lib.load(f)

    exporter, supported_args = LANGUAGE_TO_EXPORTER[args.language]

    kwargs = {}
    for arg_name in supported_args:
        arg_value = getattr(args, arg_name)
        if arg_value is not None:
            kwargs[arg_name] = arg_value

        # Special handling for the function_name parameter, which needs to be
        # the same as the default value of the keyword argument of the exporter
        # (this is due to languages like C# which prefer their method names to
        # follow PascalCase unlike all the other supported languages -- see
        # https://github.com/BayesWitnesses/m2cgen/pull/166#discussion_r379867601
        # for more).
        if arg_name == 'function_name' and arg_value is None:
            param = signature(exporter).parameters['function_name']
            kwargs[arg_name] = param.default

    return exporter(model, **kwargs)


def main():
    args = parse_args(sys.argv[1:])
    print(generate_code(args))
