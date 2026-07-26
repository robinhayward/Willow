from __future__ import annotations

import argparse
import ipaddress
import re
import shutil
import subprocess
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import ParseResult, urlparse

TEMPLATE_DIRECTORY = Path(__file__).parent.parent / "assets" / "template"
NAME_PATTERN = re.compile(r"[A-Z][A-Za-z0-9]*")
BUNDLE_ID_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9-]*(\.[A-Za-z0-9-]+)+")
HOSTNAME_PATTERN = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\."
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*"
)
TARGET_PATTERN = re.compile(
    r"(?ms)^\s*([A-F0-9]{24}) /\* ([^*]+) \*/ = \{\s*"
    r"isa = PBXNativeTarget;.*?^\s*\};"
)
ENVIRONMENTS = ("Local", "Dev", "Test", "Prod")
UNSAFE_URL_TOKENS = ("#", "$(", "${", "/*", "*/")


class GenerationError(RuntimeError):
    pass


@dataclass(frozen=True)
class ScaffoldInputs:
    name: str
    bundle_id: str
    destination: Path
    deployment_target: str
    api_urls: dict[str, str]
    web_hosts: dict[str, str]


def validate_inputs(inputs: ScaffoldInputs) -> None:
    _validate_name(inputs.name)
    _validate_bundle_id(inputs.bundle_id)
    _validate_deployment_target(inputs.deployment_target)
    _validate_urls(inputs.api_urls)
    _validate_hosts(inputs.web_hosts)
    _validate_destination(inputs.destination)


def _validate_name(name: str) -> None:
    if not NAME_PATTERN.fullmatch(name):
        raise ValueError("Name must be a Swift module beginning with an uppercase letter")


def _validate_bundle_id(bundle_id: str) -> None:
    if not BUNDLE_ID_PATTERN.fullmatch(bundle_id):
        raise ValueError("Bundle ID must be a dotted identifier")


def _validate_deployment_target(target: str) -> None:
    parts = target.split(".")
    if len(parts) != 2 or not all(part.isdigit() for part in parts):
        raise ValueError("Deployment target must be major.minor")
    if tuple(map(int, parts)) < (17, 0):
        raise ValueError("Deployment target must be at least 17.0")


def _validate_urls(api_urls: dict[str, str]) -> None:
    for environment in ENVIRONMENTS:
        _validate_url(api_urls[environment])


def _validate_url(value: str) -> None:
    parsed = _parse_url(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("API URL must use http or https and include a hostname")
    _validate_host(parsed.hostname)
    if parsed.scheme == "http" and not _is_loopback(parsed.hostname):
        raise ValueError("HTTP API URLs are allowed only for loopback hosts")


def _parse_url(value: str) -> ParseResult:
    if _has_unsafe_url_syntax(value):
        raise ValueError("API URL contains unsupported syntax")
    parsed = urlparse(value)
    _validate_url_host_and_port(parsed)
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("API URL must not include credentials")
    return parsed


def _validate_url_host_and_port(parsed: ParseResult) -> None:
    try:
        parsed.hostname
        parsed.port
    except ValueError as error:
        raise ValueError("API URL has an invalid host or port") from error
    if parsed.netloc.endswith(":"):
        raise ValueError("API URL has an invalid host or port")


def _has_unsafe_url_syntax(value: str) -> bool:
    remainder = value.partition("://")[2]
    return (
        _has_whitespace_or_control(value)
        or any(token in value for token in UNSAFE_URL_TOKENS)
        or "//" in remainder
    )


def _has_whitespace_or_control(value: str) -> bool:
    return any(
        character.isspace() or unicodedata.category(character) == "Cc"
        for character in value
    )


def _is_loopback(host: str) -> bool:
    if host.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def _validate_hosts(web_hosts: dict[str, str]) -> None:
    for environment in ENVIRONMENTS:
        _validate_host(web_hosts[environment])


def _validate_host(host: str) -> None:
    if host != host.strip() or any(character in host for character in "/?#@"):
        raise ValueError("Web host must be a hostname or IP address")
    if _is_ip_address(host) or HOSTNAME_PATTERN.fullmatch(host):
        return
    raise ValueError("Web host must be a hostname or IP address")


def _is_ip_address(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _validate_destination(destination: Path) -> None:
    if destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
        raise ValueError("Destination is not empty")


def _require_xcodegen() -> None:
    if not shutil.which("xcodegen"):
        raise GenerationError("xcodegen is required but was not found on PATH")


def xcconfig_url(url: str) -> str:
    return url.replace("://", ":/$()/", 1)


def render_template(inputs: ScaffoldInputs, destination: Path) -> None:
    replacements = _template_replacements(inputs)
    for source in sorted(TEMPLATE_DIRECTORY.rglob("*")):
        target = destination / _render_path(source.relative_to(TEMPLATE_DIRECTORY), replacements)
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(_render(source.read_text(encoding="utf-8"), replacements), encoding="utf-8")


def _template_replacements(inputs: ScaffoldInputs) -> dict[str, str]:
    return {
        "__APP__": inputs.name,
        "__BUNDLE_ID__": inputs.bundle_id,
        "__DEPLOYMENT_TARGET__": inputs.deployment_target,
        "__LOCAL_API_URL__": xcconfig_url(inputs.api_urls["Local"]),
        "__LOCAL_WEB_HOST__": inputs.web_hosts["Local"],
        "__DEV_API_URL__": xcconfig_url(inputs.api_urls["Dev"]),
        "__DEV_WEB_HOST__": inputs.web_hosts["Dev"],
        "__TEST_API_URL__": xcconfig_url(inputs.api_urls["Test"]),
        "__TEST_WEB_HOST__": inputs.web_hosts["Test"],
        "__PROD_API_URL__": xcconfig_url(inputs.api_urls["Prod"]),
        "__PROD_WEB_HOST__": inputs.web_hosts["Prod"],
    }


def _render_path(path: Path, replacements: dict[str, str]) -> Path:
    return Path(*(_render(component, replacements) for component in path.parts))


def _render(value: str, replacements: dict[str, str]) -> str:
    for placeholder, replacement in replacements.items():
        value = value.replace(placeholder, replacement)
    return value


def generate_project(inputs: ScaffoldInputs) -> None:
    validate_inputs(inputs)
    _require_xcodegen()
    with tempfile.TemporaryDirectory(dir=inputs.destination.parent) as temporary_directory:
        temporary_app = Path(temporary_directory)
        render_template(inputs, temporary_app)
        run_xcodegen(temporary_app)
        _rewrite_test_plan(inputs, temporary_app)
        _replace_destination(inputs.destination, temporary_app)


def run_xcodegen(project_directory: Path) -> None:
    try:
        subprocess.run(
            ["xcodegen", "generate", "--spec", "project.yml", "--project", str(project_directory)],
            cwd=project_directory,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        raise GenerationError(error.stderr) from error


def _rewrite_test_plan(inputs: ScaffoldInputs, project_directory: Path) -> None:
    target_ids = _native_target_ids(project_directory / f"{inputs.name}.xcodeproj" / "project.pbxproj")
    plan = project_directory / "Tests" / f"{inputs.name}.xctestplan"
    plan.write_text(
        plan.read_text(encoding="utf-8")
        .replace("__APP_TARGET_ID__", _target_id(target_ids, inputs.name))
        .replace("__UI_TEST_TARGET_ID__", _target_id(target_ids, f"{inputs.name}UITests")),
        encoding="utf-8",
    )


def _native_target_ids(project_file: Path) -> dict[str, str]:
    target_ids = {name: identifier for identifier, name in TARGET_PATTERN.findall(project_file.read_text())}
    if not target_ids:
        raise GenerationError("XcodeGen project contains no native targets")
    return target_ids


def _target_id(target_ids: dict[str, str], target_name: str) -> str:
    try:
        return target_ids[target_name]
    except KeyError as error:
        raise GenerationError(f"XcodeGen project is missing target {target_name}") from error


def _replace_destination(destination: Path, temporary_app: Path) -> None:
    if destination.exists():
        destination.rmdir()
    temporary_app.rename(destination)


def parse_args(arguments: list[str] | None = None) -> ScaffoldInputs:
    parser = argparse.ArgumentParser(description="Create a modular SwiftUI iOS app")
    parser.add_argument("--name", required=True)
    parser.add_argument("--bundle-id", required=True)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--deployment-target", required=True)
    for environment in ("local", "dev", "test", "prod"):
        parser.add_argument(f"--{environment}-api-url", required=True)
        parser.add_argument(f"--{environment}-web-host", required=True)
    values = parser.parse_args(arguments)
    return ScaffoldInputs(
        name=values.name,
        bundle_id=values.bundle_id,
        destination=values.destination,
        deployment_target=values.deployment_target,
        api_urls={
            environment: getattr(values, f"{environment.lower()}_api_url")
            for environment in ENVIRONMENTS
        },
        web_hosts={
            environment: getattr(values, f"{environment.lower()}_web_host")
            for environment in ENVIRONMENTS
        },
    )


def main() -> int:
    try:
        inputs = parse_args()
        generate_project(inputs)
    except (GenerationError, ValueError) as error:
        print(error)
        return 1
    print(f"Created {(inputs.destination.resolve() / f'{inputs.name}.xcodeproj')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
