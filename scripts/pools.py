"""The five script pools of this series (spec.md, "Scripts and pools").

The mechanics live in ``synoptic.script_pool``; this file holds only the
concrete definitions and the CLI:

    .venv/bin/python scripts/pools.py --pool devanagari
    .venv/bin/python scripts/pools.py --pool latin-bantu --nt-only-except sna

Run the data-licence-check skill whenever selections are (re)built.
"""

import argparse

from synoptic.script_pool import PoolSpec, build_pool, write_pool

POOLS: dict[str, PoolSpec] = {
    # marc duplicates Marathi: with mar a target its OT/test text would leak.
    "devanagari": PoolSpec(script="Devanagari", targets=["hne", "mar"], exclude=["marc"]),
    # Both Standard Arabic texts stay: arb is not a target, and two renderings
    # of the strongest language enrich the pool.
    "arabic": PoolSpec(script="Arabic", targets=["ckb", "urdoucv"]),
    "ethiopic": PoolSpec(script="Ethiopic", targets=["gmve", "gofe"]),
    "telugu": PoolSpec(script="Telugu", targets=["nit", "vgr"]),
    # Family-coherent Latin control, profile-matched to Devanagari (spec.md).
    "latin-bantu": PoolSpec(
        script="Latin",
        targets=["nde", "nya"],
        languages=["kik", "lin", "lug", "nde", "nya", "sna", "swh"],
        one_per_language=True,
    ),
}


def main() -> None:
    ap = argparse.ArgumentParser(description="Build a by-script pool selection")
    ap.add_argument("--pool", required=True, choices=sorted(POOLS))
    ap.add_argument(
        "--nt-only-except", default=None,
        help="comma-separated ids exempt from NT truncation (the chosen "
             "source); targets are always exempt. Omit for no truncation.",
    )
    args = ap.parse_args()

    exempt = args.nt_only_except.split(",") if args.nt_only_except else None
    selection = build_pool(POOLS[args.pool], nt_only_except=exempt)
    out = write_pool(selection, args.pool)
    n = selection["languageCode"].nunique()
    print(f"Wrote {out}: {len(selection)} translations, {n} languages")
    print(selection[["translationId", "languageCode", "OTverses", "NTverses",
                     "licence", "ntOnly"]].to_string(index=False))


if __name__ == "__main__":
    main()
