from __future__ import annotations

import ast
import csv

from collections import defaultdict
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path.cwd()

OUTPUT_DIR = (
    PROJECT_ROOT
    / "_Dependency_Report"
)

IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "_Dependency_Report",
}

PROJECT_PREFIXES = (
    "core",
    "runtime",
    "database",
    "config",
    "utils",
    "tests",
)

ORPHAN_EXCLUSIONS = {
    "main",
    "tree",
    "PROJECT_DEPENDENCY_ANALYZER",
}

ORPHAN_PREFIX_EXCLUSIONS = [
    "tests.",
]

def discover_python_files() -> list[Path]:

    files: list[Path] = []

    for file in PROJECT_ROOT.rglob("*.py"):

        skip = False

        for part in file.parts:

            if part in IGNORE_DIRS:

                skip = True

                break

        if skip:

            continue

        files.append(file)

    return sorted(files)

def module_name_from_path(
    file_path: Path
) -> str:

    relative = (
        file_path.relative_to(
            PROJECT_ROOT
        )
    )

    return ".".join(
        relative.with_suffix("").parts
    )
    
def extract_imports(
    file_path: Path
) -> tuple[set[str], int]:

    imports: set[str] = set()

    external_imports = 0

    try:

        source = file_path.read_text(
            encoding="utf-8"
        )

        tree = ast.parse(source)

        for node in ast.walk(tree):

            if isinstance(
                node,
                ast.Import
            ):

                for alias in node.names:

                    if alias.name.startswith(
                        PROJECT_PREFIXES
                    ):

                        imports.add(
                            alias.name
                        )

                    else:

                        external_imports += 1

            elif isinstance(
                node,
                ast.ImportFrom
            ):

                if not node.module:

                    continue

                if node.module.startswith(
                    PROJECT_PREFIXES
                ):

                    imports.add(
                        node.module
                    )

                else:

                    external_imports += 1

    except Exception as error:

        print(
            f"[ERROR] "
            f"{file_path}: "
            f"{error}"
        )

    return (
        imports,
        external_imports
    )

def is_candidate_orphan(
    module: str
) -> bool:

    if module in ORPHAN_EXCLUSIONS:

        return False

    if module.endswith(
        "__init__"
    ):

        return False

    for prefix in (
        ORPHAN_PREFIX_EXCLUSIONS
    ):

        if module.startswith(
            prefix
        ):

            return False

    return True
def write_import_summary(
    dependencies: dict[
        str,
        set[str]
    ]
) -> None:

    output = (
        OUTPUT_DIR
        / "import_summary.csv"
    )

    with open(
        output,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(
            file
        )

        writer.writerow(
            [
                "Source Module",
                "Imported Module"
            ]
        )

        for source in sorted(
            dependencies
        ):

            for target in sorted(
                dependencies[source]
            ):

                writer.writerow(
                    [
                        source,
                        target
                    ]
                )

def write_reverse_dependencies(
    reverse_map: dict[
        str,
        set[str]
    ]
) -> None:

    output = (
        OUTPUT_DIR
        / "reverse_dependencies.csv"
    )

    with open(
        output,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(
            file
        )

        writer.writerow(
            [
                "Module",
                "Used By"
            ]
        )

        for module in sorted(
            reverse_map
        ):

            for user in sorted(
                reverse_map[module]
            ):

                writer.writerow(
                    [
                        module,
                        user
                    ]
                )
def write_orphans(
    modules: set[str],
    reverse_map: dict[
        str,
        set[str]
    ]
) -> int:

    output = (
        OUTPUT_DIR
        / "orphan_files.txt"
    )

    orphan_count = 0

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "Potential Orphan Files\n"
        )

        file.write(
            "=" * 60
        )

        file.write(
            "\n\n"
        )

        for module in sorted(
            modules
        ):

            if not (
                is_candidate_orphan(
                    module
                )
            ):

                continue

            if module not in reverse_map:

                orphan_count += 1

                file.write(
                    f"{module}\n"
                )

    return orphan_count
def write_high_risk_modules(
    reverse_map: dict[
        str,
        set[str]
    ]
) -> None:

    output = (
        OUTPUT_DIR
        / "high_risk_modules.txt"
    )

    ranking = []

    for module in reverse_map:

        ranking.append(
            (
                module,
                len(
                    reverse_map[module]
                )
            )
        )

    ranking.sort(
        key=lambda x: x[1],
        reverse=True
    )

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "HIGH RISK MODULES\n"
        )

        file.write(
            "=" * 60
        )

        file.write(
            "\n\n"
        )

        for module, count in ranking:

            file.write(
                f"{count:>4}  "
                f"{module}\n"
            )
def write_runtime_dependencies(
    dependencies: dict[
        str,
        set[str]
    ]
) -> None:

    output = (
        OUTPUT_DIR
        / "runtime_dependencies.txt"
    )

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as file:

        for module in sorted(
            dependencies
        ):

            if not module.startswith(
                "runtime."
            ):

                continue

            file.write(
                f"{module}\n\n"
            )

            for dependency in sorted(
                dependencies[module]
            ):

                file.write(
                    f"    {dependency}\n"
                )

            file.write(
                "\n"
                + "-" * 60
                + "\n\n"
            )
def write_architecture_report(
    modules: set[str]
) -> None:

    output = (
        OUTPUT_DIR
        / "architecture_report.md"
    )

    sections = defaultdict(
        list
    )

    for module in modules:

        top = module.split(".")[0]

        sections[top].append(
            module
        )

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "# Architecture Report\n\n"
        )

        for section in sorted(
            sections
        ):

            file.write(
                f"## {section}\n\n"
            )

            for module in sorted(
                sections[section]
            ):

                file.write(
                    f"- {module}\n"
                )

            file.write(
                "\n"
            )
def write_statistics(
    file_count: int,
    internal_imports: int,
    external_imports: int,
    orphan_count: int
) -> None:

    output = (
        OUTPUT_DIR
        / "statistics.txt"
    )

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "Project Statistics\n"
        )

        file.write(
            "=" * 60
        )

        file.write(
            "\n\n"
        )

        file.write(
            f"Python Files: "
            f"{file_count}\n"
        )

        file.write(
            f"Internal Imports: "
            f"{internal_imports}\n"
        )

        file.write(
            f"External Imports: "
            f"{external_imports}\n"
        )

        file.write(
            f"Orphan Files: "
            f"{orphan_count}\n"
        )

        file.write(
            "\nGenerated:\n"
        )

        file.write(
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
def main() -> None:

    print(
        "\n=== DEPENDENCY ANALYZER ===\n"
    )

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    files = (
        discover_python_files()
    )

    modules: set[str] = set()

    dependencies = {}

    reverse_map = defaultdict(
        set
    )

    internal_imports = 0

    external_imports = 0

    for file in files:

        module = (
            module_name_from_path(
                file
            )
        )

        modules.add(
            module
        )

        imports, external = (
            extract_imports(
                file
            )
        )

        dependencies[module] = (
            imports
        )

        internal_imports += len(
            imports
        )

        external_imports += (
            external
        )

        for imported in imports:

            reverse_map[
                imported
            ].add(
                module
            )

    orphan_count = (
        write_orphans(
            modules,
            reverse_map
        )
    )

    write_import_summary(
        dependencies
    )

    write_reverse_dependencies(
        reverse_map
    )

    write_high_risk_modules(
        reverse_map
    )

    write_runtime_dependencies(
        dependencies
    )

    write_architecture_report(
        modules
    )

    write_statistics(
        file_count=len(files),
        internal_imports=(
            internal_imports
        ),
        external_imports=(
            external_imports
        ),
        orphan_count=(
            orphan_count
        )
    )

    print(
        f"Files: {len(files)}"
    )

    print(
        f"Internal Imports: "
        f"{internal_imports}"
    )

    print(
        f"External Imports: "
        f"{external_imports}"
    )

    print(
        f"Orphans: "
        f"{orphan_count}"
    )

    print(
        "\nOutput:"
    )

    print(
        OUTPUT_DIR
    )

    print(
        "\n=== COMPLETE ==="
    )


if __name__ == "__main__":
    main()