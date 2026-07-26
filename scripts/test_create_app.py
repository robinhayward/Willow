from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS_DIRECTORY = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIRECTORY))

from create_app import (  # noqa: E402
    GenerationError,
    ScaffoldInputs,
    generate_project,
    validate_inputs,
)


def valid_inputs(
    *, name: str = "SampleApp", destination: Path | None = None
) -> ScaffoldInputs:
    return ScaffoldInputs(
        name=name,
        bundle_id="com.example.sampleapp",
        destination=destination or Path("SampleApp"),
        deployment_target="17.0",
        api_urls={
            "Local": "http://localhost:8000",
            "Dev": "https://dev.example.invalid",
            "Test": "https://test.example.invalid",
            "Prod": "https://api.example.invalid",
        },
        web_hosts={
            "Local": "localhost",
            "Dev": "dev.example.invalid",
            "Test": "test.example.invalid",
            "Prod": "example.invalid",
        },
    )


def inputs_with_api_url(api_url: str) -> ScaffoldInputs:
    inputs = valid_inputs()
    inputs.api_urls["Dev"] = api_url
    return inputs


def fake_xcodegen(project_directory: Path) -> None:
    project = project_directory / "SampleApp.xcodeproj"
    project.mkdir()
    (project / "project.pbxproj").write_text(
        """\
/* Begin PBXNativeTarget section */
\t\tABCDEF0123456789ABCDEF01 /* SampleApp */ = {
\t\t\tisa = PBXNativeTarget;
\t\t\tname = SampleApp;
\t\t};
\t\t0123456789ABCDEF01234567 /* SampleAppUITests */ = {
\t\t\tisa = PBXNativeTarget;
\t\t\tname = SampleAppUITests;
\t\t};
/* End PBXNativeTarget section */
"""
    )


class CreateAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.template_directory = tempfile.TemporaryDirectory()
        template = Path(self.template_directory.name)
        (template / "Tests").mkdir()
        (template / "project.yml").write_text("name: __APP__\ncore: __APP__Core\n")
        (template / "Tests" / "__APP__.xctestplan").write_text(
            "app: __APP_TARGET_ID__\nui: __UI_TEST_TARGET_ID__\n"
        )
        self.template_patch = patch("create_app.TEMPLATE_DIRECTORY", template)
        self.template_patch.start()
        self.addCleanup(self.template_patch.stop)
        self.addCleanup(self.template_directory.cleanup)

    def test_rejects_invalid_module_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "Swift module"):
            validate_inputs(valid_inputs(name="not valid"))

    def test_rejects_existing_nonempty_destination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "App"
            destination.mkdir()
            (destination / "keep.txt").write_text("owned")
            with self.assertRaisesRegex(ValueError, "not empty"):
                validate_inputs(valid_inputs(destination=destination))

    def test_api_urls_are_safe_xcconfig_values(self) -> None:
        valid_urls = (
            "https://api.example.invalid",
            "https://api.example.invalid:443/v1/items?limit=10",
            "https://192.0.2.1:8443/v1",
            "https://[2001:db8::1]:8443/v1",
            "http://localhost:8000/v1?limit=10",
            "http://127.0.0.1:8080",
            "http://[::1]:8080",
        )
        invalid_urls = (
            "https://bad_host.example.invalid",
            "https://example.invalid:not-a-port",
            "https://example.invalid:",
            "https://example.invalid:65536",
            "https://user:secret@example.invalid",
            "https://example.invalid/has space",
            "https://example.invalid/\tcontrol",
            "https://example.invalid/\ncontrol",
            "https://example.invalid/path#fragment",
            "https://example.invalid/path?value=$(SECRET)",
            "https://example.invalid/?value=${SECRET}",
            "https://example.invalid/*comment",
            "https://example.invalid/comment*/tail",
            "https://example.invalid/path//nested",
            "http://example.invalid",
        )

        for url in valid_urls:
            with self.subTest(url=url):
                validate_inputs(inputs_with_api_url(url))
        for url in invalid_urls:
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    validate_inputs(inputs_with_api_url(url))

    def test_generation_is_atomic_and_renders_names(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            inputs = valid_inputs(destination=Path(directory) / "SampleApp")
            with (
                patch("create_app.shutil.which", return_value="xcodegen"),
                patch("create_app.run_xcodegen", side_effect=fake_xcodegen),
            ):
                generate_project(inputs)
            self.assertTrue((inputs.destination / "SampleApp.xcodeproj").is_dir())
            self.assertIn("SampleAppCore", (inputs.destination / "project.yml").read_text())

    def test_failed_xcodegen_leaves_destination_absent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            inputs = valid_inputs(destination=Path(directory) / "SampleApp")
            with (
                patch("create_app.shutil.which", return_value="xcodegen"),
                patch(
                    "create_app.run_xcodegen", side_effect=GenerationError("failed")
                ),
            ):
                with self.assertRaises(GenerationError):
                    generate_project(inputs)
            self.assertFalse(inputs.destination.exists())
