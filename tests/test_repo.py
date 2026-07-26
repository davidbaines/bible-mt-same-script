"""Repo-level checks: configs load, pools match committed selections."""

import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest
import yaml

from synoptic.config import ExperimentConfig
from synoptic.data_pipeline import load_vref_list

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from pools import POOLS  # noqa: E402


def experiment_configs() -> list[Path]:
    return sorted((REPO / "configs" / "experiments").glob("*.yaml"))


def test_every_experiment_config_loads_and_resolves():
    configs = experiment_configs()
    assert configs, "no experiment configs generated yet"
    for path in configs:
        cfg = ExperimentConfig.load(path)
        assert (REPO / cfg.data.selection).exists(), f"{path.name}: missing selection"
        holdouts = yaml.safe_load((REPO / cfg.data.holdouts).read_text())
        assert holdouts["holdouts"], f"{path.name}: empty holdouts"
        assert cfg.data.source, f"{path.name}: no source set"
        assert cfg.data.companion_ranking == "coverage"
        if cfg.validation is not None and "smoke" not in path.name:
            assert cfg.validation.min_gain == 0.2
            assert cfg.validation.patience_steps == 4000


def test_sources_never_held_out():
    for path in experiment_configs():
        cfg = ExperimentConfig.load(path)
        holdouts = yaml.safe_load((REPO / cfg.data.holdouts).read_text())
        held = set(holdouts["holdouts"]) | set(holdouts.get("verse_holdouts") or {})
        assert cfg.data.source not in held, f"{path.name}: source is held out"


def test_gen250_list_is_250_genesis_verses():
    vrefs = load_vref_list(REPO / "configs" / "test-verses-gen250.txt")
    assert len(vrefs) == 250
    assert all(v.startswith("GEN ") for v in vrefs)


def test_selections_match_pool_specs():
    for pool, spec in POOLS.items():
        sel = pd.read_csv(REPO / "experiments" / f"selection-{pool}.csv")
        ids = set(sel["translationId"])
        assert set(spec.targets) <= ids, f"{pool}: targets missing from selection"
        assert not (set(spec.exclude) & ids), f"{pool}: excluded id present"
        assert (sel["licence"].isin(["Public Domain", "by", "by-sa"])).all()


@pytest.mark.integration
def test_make_configs_reproduces_committed_files():
    """Regeneration must be a no-op against the committed tree.

    Runs the generator in place, then asserts git sees no changes under the
    generated paths — catching both non-determinism and drift between the
    committed configs and the current generator/metadata.
    """
    def generated_dirt() -> str:
        return subprocess.run(
            ["git", "-C", str(REPO), "status", "--porcelain", "--",
             "configs", "experiments/selection-latin-bantu.csv"],
            capture_output=True, text=True,
        ).stdout.strip()

    pre = generated_dirt()
    assert not pre, (
        "working tree already has local edits under the generated paths; "
        f"commit or stash them before this test:\n{pre}"
    )
    r = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "make_configs.py")],
        capture_output=True, text=True, cwd=REPO,
    )
    assert r.returncode == 0, r.stderr
    assert "wrote 22 experiment configs" in r.stdout
    dirty = generated_dirt()
    assert not dirty, f"regeneration changed committed files:\n{dirty}"
    # Deletion gap: every committed experiment YAML must be one the generator
    # (or the hand-written smoke config) still owns.
    written = {ln.split()[-1] for ln in r.stdout.splitlines() if ln.startswith("  ")}
    committed = {p.stem for p in (REPO / "configs" / "experiments").glob("*.yaml")}
    stale = committed - written - {"smoke"}
    assert not stale, f"committed configs no longer generated: {sorted(stale)}"
