"""Automated documentation, YAML/Jinja2 syntax, and role parity verification suite."""

from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys
import unittest

import jinja2
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"

FENCE_RE = re.compile(r"^([ \t]*)(`{3,}|~{3,})(.*)$")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
BOX_OR_ARROW_RE = re.compile(r"(?:[┌┐└┘╔╗╚╝├┤┬┴┼═─]{2,}|\+[-=]{2,}\+|(?<![<!])-->|<--)")
INDENTED_MERMAID_RE = re.compile(r"^[ \t]+(?:```|~~~)mermaid\b", re.MULTILINE)
UNFENCED_MERMAID_HEADER_RE = re.compile(r"^(?:flowchart|graph\s+(?:TD|TB|LR)|sequenceDiagram)\b")

WEAK_MODALS_RE = re.compile(r"\b(?:should|would|may|might|shall|ought)\b", re.IGNORECASE)
CONTRACTIONS_RE = re.compile(
    r"\b(?:don't|doesn't|didn't|won't|can't|isn't|aren't|wasn't|weren't|"
    r"haven't|hasn't|hadn't|you're|we're|they're|it's|that's)\b",
    re.IGNORECASE,
)
FRENCH_STOPWORD_RE = re.compile(
    r"[àâäçéèêëîïôöùûüÿœæ]|"
    r"\b(?:procédure|tutoriel|prérequis|étape|vérification|déploiement|référence)\b",
    re.IGNORECASE,
)


def _strip_code_blocks(text: str) -> str:
    """Return markdown prose with fenced code blocks removed."""
    kept: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if not in_fence and match:
            in_fence = True
            fence_char = match.group(2)[0]
            fence_len = len(match.group(2))
            continue
        if in_fence:
            stripped = line.strip()
            if stripped and set(stripped) == {fence_char} and len(stripped) >= fence_len:
                in_fence = False
            continue
        kept.append(line)
    return "\n".join(kept)


def _project_markdown_files() -> list[pathlib.Path]:
    """List tracked repository markdown files outside build or git directories."""
    excluded = {".git", "venv", ".venv", "site", "node_modules"}
    return sorted(
        path
        for path in REPO_ROOT.rglob("*.md")
        if not any(part in excluded for part in path.parts)
    )


class TestDocsTutorialsHowtos(unittest.TestCase):
    """Validate cleanup, Diataxis governance, YAML/Jinja2 syntax, and role parity."""

    def test_no_committed_virtualenv_and_valid_gitignore(self) -> None:
        gitignore_text = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        lines = [line.strip() for line in gitignore_text.splitlines()]
        self.assertIn("venv/", lines)
        self.assertNotIn("venv/** */", lines)
        self.assertFalse((REPO_ROOT / "venv").exists())

        if (REPO_ROOT / ".git").exists() and shutil.which("git"):
            result = subprocess.run(
                ["git", "-C", str(REPO_ROOT), "ls-files", "venv"],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertEqual(result.stdout.strip(), "", "venv files must not be tracked")

    def test_all_yaml_files_parse_cleanly(self) -> None:
        yaml_files = sorted(
            p
            for ext in ("*.yml", "*.yaml")
            for p in REPO_ROOT.rglob(ext)
            if ".git" not in p.parts and "venv" not in p.parts
        )
        self.assertGreater(len(yaml_files), 50)
        for path in yaml_files:
            with self.subTest(file=str(path.relative_to(REPO_ROOT))):
                yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_all_jinja2_templates_parse_cleanly(self) -> None:
        env = jinja2.Environment()
        templates = sorted((REPO_ROOT / "roles").rglob("*.j2"))
        self.assertGreaterEqual(len(templates), 5)
        for template_path in templates:
            with self.subTest(template=str(template_path.relative_to(REPO_ROOT))):
                env.parse(template_path.read_text(encoding="utf-8"))

    def test_shell_scripts_syntax_and_portability(self) -> None:
        scripts = sorted(
            p for p in REPO_ROOT.rglob("*.sh") if ".git" not in p.parts and "venv" not in p.parts
        )
        self.assertGreaterEqual(len(scripts), 3)
        bash_bin = shutil.which("bash")
        for script_path in scripts:
            content = script_path.read_text(encoding="utf-8")
            self.assertNotIn("/home/jmren/", content, f"Hardcoded home path in {script_path}")
            if bash_bin:
                # Pass LF bytes via stdin so `bash -n` works identically under Windows WSL and Linux.
                proc = subprocess.run(
                    [bash_bin, "-n"],
                    input=content.replace("\r\n", "\n").encode("utf-8"),
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(
                    proc.returncode,
                    0,
                    f"bash -n failed for {script_path}: {proc.stderr.decode('utf-8', 'replace')}",
                )

    def test_diataxis_structure_links_and_ste_rules(self) -> None:
        for rel in (
            "index.md",
            "01-tutorials/index.md",
            "01-tutorials/01-standalone-and-docker-lab.md",
            "01-tutorials/02-replica-set-and-tls.md",
            "02-how-to-guides/index.md",
            "02-how-to-guides/deploy-replica-set-and-sharding.md",
            "02-how-to-guides/backup-upgrade-and-tls-operations.md",
            "03-reference/index.md",
            "03-reference/variables-playbooks-and-scenarios.md",
            "04-explanation/index.md",
            "04-explanation/role-architecture-and-quorum-design.md",
        ):
            self.assertTrue((DOCS_DIR / rel).is_file(), f"Missing Diataxis page docs/{rel}")

        # Verify relative links across user-facing markdown documents.
        doc_pages = [
            REPO_ROOT / "README.md",
            REPO_ROOT / "TEST_SPECIFICATIONS.md",
            REPO_ROOT / "docker/README.md",
            *sorted((REPO_ROOT / "documentation").glob("*.md")),
            *sorted(DOCS_DIR.rglob("*.md")),
        ]
        for page in doc_pages:
            prose = _strip_code_blocks(page.read_text(encoding="utf-8"))
            self.assertNotIn("file:///", prose, f"Local file URI left in {page}")
            for target in LINK_RE.findall(prose):
                clean = target.split("#", 1)[0].strip()
                if not clean or clean.startswith(("http://", "https://", "mailto:")):
                    continue
                resolved = (page.parent / clean).resolve()
                self.assertTrue(
                    resolved.exists(),
                    f"Broken relative link '{target}' in {page.relative_to(REPO_ROOT)}",
                )

        # Enforce STE structural rules and quadrant hygiene on 02-how-to-guides/ and 04-explanation/.
        for guide in sorted((DOCS_DIR / "02-how-to-guides").glob("*.md")):
            if guide.name == "index.md":
                continue
            prose = _strip_code_blocks(guide.read_text(encoding="utf-8"))
            self.assertIsNone(WEAK_MODALS_RE.search(prose), f"Weak modal in {guide}")
            self.assertIsNone(CONTRACTIONS_RE.search(prose), f"Contraction in {guide}")
            self.assertNotIn(";", prose, f"Semicolon in {guide}")
            self.assertFalse(re.search(r"^##\s+(?:Why|Architecture|Context)\b", prose, re.M))
            for raw_line in prose.splitlines():
                line = raw_line.strip()
                if not line or line.startswith(("#", "|", ">", "```")):
                    continue
                clean_line = re.sub(r"`[^`]+`", "CODE", re.sub(r"^\d+\.\s*", "", line))
                clean_line = re.sub(r"\*\*[^*]+:\*\*\s*", "", clean_line)
                for sentence in re.split(r"(?<=[.!?])\s+", clean_line):
                    words = [w for w in sentence.strip().split() if w]
                    self.assertLessEqual(
                        len(words),
                        25,
                        f"Overlong STE sentence ({len(words)} words) in {guide.name}: {sentence}",
                    )

        for exp in sorted((DOCS_DIR / "04-explanation").glob("*.md")):
            if exp.name == "index.md":
                continue
            prose = _strip_code_blocks(exp.read_text(encoding="utf-8"))
            self.assertFalse(re.search(r"^##\s+Step\s+\d+", prose, re.M), f"Tutorial step in {exp}")

    def test_optional_skill_validators_if_installed(self) -> None:
        skills_root = pathlib.Path.home() / ".gemini/config/skills"
        diataxis_script = skills_root / "diataxis-docs/scripts/diataxis_check.py"
        if diataxis_script.is_file():
            proc = subprocess.run(
                [sys.executable, str(diataxis_script), str(DOCS_DIR), "--strict", "--check-ste", "--lang", "en"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("0 error(s), 0 warning(s)", proc.stdout)

        ste_script = skills_root / "simplified-technical-english/scripts/ste_check.py"
        if ste_script.is_file():
            guides = sorted(
                str(p)
                for p in (DOCS_DIR / "02-how-to-guides").glob("*.md")
                if p.name != "index.md"
            )
            proc = subprocess.run(
                [sys.executable, str(ste_script), "--mode", "procedural", *guides],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("Result: 0 errors, 0 warnings.", proc.stdout)

    def test_diagrams_mermaid_no_ascii_and_english_only(self) -> None:
        mermaid_count = 0
        for md_path in _project_markdown_files():
            raw = md_path.read_text(encoding="utf-8")
            self.assertIsNone(
                INDENTED_MERMAID_RE.search(raw),
                f"Indented mermaid fence found in {md_path.relative_to(REPO_ROOT)}",
            )
            in_fence = False
            fence_info = ""
            fence_char = ""
            fence_len = 0
            for idx, line in enumerate(raw.splitlines(), start=1):
                match = FENCE_RE.match(line)
                if not in_fence and match:
                    in_fence = True
                    fence_char = match.group(2)[0]
                    fence_len = len(match.group(2))
                    fence_info = match.group(3).strip().lower()
                    if fence_info == "mermaid":
                        mermaid_count += 1
                    continue
                if in_fence:
                    stripped = line.strip()
                    if stripped and set(stripped) == {fence_char} and len(stripped) >= fence_len:
                        in_fence = False
                        fence_info = ""
                        continue
                    if fence_info == "mermaid":
                        continue
                    if fence_info in ("", "text", "txt", "ascii"):
                        self.assertIsNone(
                            UNFENCED_MERMAID_HEADER_RE.match(line.strip()),
                            f"Mermaid syntax inside non-mermaid fence at {md_path}:{idx}",
                        )
                        self.assertIsNone(
                            BOX_OR_ARROW_RE.search(line),
                            f"ASCII/box diagram found at {md_path}:{idx}: {line}",
                        )
                    continue

                if "-->" not in line and "<--" not in line:
                    self.assertIsNone(
                        BOX_OR_ARROW_RE.search(line),
                        f"Box/ASCII art line in {md_path}:{idx}: {line}",
                    )
                else:
                    # Allow only prose arrow notes outside ASCII diagram blocks when explicitly HTML comments.
                    no_comments = re.sub(r"<!--[\s\S]*?-->", "", line)
                    no_inline = re.sub(r"`[^`]+`", "", no_comments)
                    if "-->" in no_inline and not any(tok in no_inline for tok in ("->", "Arbiter ->")):
                        self.assertFalse(
                            bool(re.search(r"(?:^|\s)-->(?:\s|$)", no_inline)),
                            f"Unfenced diagram arrow in {md_path}:{idx}",
                        )

            prose = _strip_code_blocks(raw)
            self.assertIsNone(
                FRENCH_STOPWORD_RE.search(prose),
                f"Unexpected French text in {md_path.relative_to(REPO_ROOT)}",
            )

        self.assertGreaterEqual(mermaid_count, 4)

    def test_documented_defaults_playbooks_and_scenarios_parity(self) -> None:
        defaults = yaml.safe_load((REPO_ROOT / "roles/mongod/defaults/main.yml").read_text(encoding="utf-8"))
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        params_doc = (REPO_ROOT / "documentation/PARAMETERS.md").read_text(encoding="utf-8")
        ref_doc = (DOCS_DIR / "03-reference/variables-playbooks-and-scenarios.md").read_text(encoding="utf-8")

        for var_name in defaults:
            self.assertIn(var_name, params_doc, f"{var_name} missing in documentation/PARAMETERS.md")
            self.assertIn(var_name, ref_doc, f"{var_name} missing in docs/03-reference/")

        self.assertIn("mongodb_version: 6.0", readme)
        self.assertIn("`6.0`", params_doc)
        self.assertIn("`6.0`", ref_doc)
        self.assertIn("any_errors_fatal: true", readme)
        self.assertNotIn("any_error_true", readme)

        playbooks = sorted(p.name for p in (REPO_ROOT / "playbooks").glob("*.yml"))
        self.assertGreaterEqual(len(playbooks), 4)
        for pb in playbooks:
            self.assertIn(f"playbooks/{pb}", readme, f"playbooks/{pb} missing in README.md")
            self.assertIn(f"playbooks/{pb}", ref_doc, f"playbooks/{pb} missing in reference doc")

        scenarios = sorted(
            p.name for p in (REPO_ROOT / "roles/mongod/molecule").iterdir() if p.is_dir()
        )
        self.assertGreaterEqual(len(scenarios), 8)
        for sc in scenarios:
            self.assertIn(sc, readme, f"Scenario {sc} missing in README.md")
            self.assertIn(sc, ref_doc, f"Scenario {sc} missing in reference doc")
            mol_text = (REPO_ROOT / "roles/mongod/molecule" / sc / "molecule.yml").read_text(encoding="utf-8")
            self.assertNotIn("s../../roles", mol_text, f"Corrupted cgroup mount left in {sc}/molecule.yml")

        docker_mk = (REPO_ROOT / "docker/Makefile").read_text(encoding="utf-8")
        for target in ("build", "network", "run", "stop", "clean"):
            self.assertRegex(docker_mk, re.compile(rf"^{target}:", re.MULTILINE))
            self.assertIn(f"make {target}", ref_doc)

        tut1 = (DOCS_DIR / "01-tutorials/01-standalone-and-docker-lab.md").read_text(encoding="utf-8")
        self.assertIn('--private-key docker/id_rsa', tut1)
        self.assertIn('-e \'{"mongodb_backup":{"pass":"lab_backup_secret"}}\'', tut1)


if __name__ == "__main__":
    unittest.main()
