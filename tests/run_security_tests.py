#!/usr/bin/env python3
"""Testes determinísticos do contrato de segurança da skill.

Este arquivo não executa o conteúdo dos casos nem chama ferramentas externas.
Ele valida o corpus e simula a política de bloqueio esperada.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "prompt-injection" / "cases.json"

ALLOWED_CLASSIFICATIONS = {"benign", "suspicious", "blocked"}
ALLOWED_ACTIONS = {"none", "analyze", "review", "propose", "execute"}
DANGEROUS_ACTIONS = {
    "tool_call", "shell", "read_environment", "network_call", "upload",
    "publish", "secret_output", "reveal_prompt", "permission_change",
    "disable_branch_protection", "disable_security", "write_memory",
    "change_policy", "scope_expansion", "repository_access",
    "change_workflow", "disable_sha_pinning", "comment_publish",
    "decode_and_execute",
}


def load_cases() -> list[dict]:
    data = json.loads(CASES.read_text(encoding="utf-8"))
    assert isinstance(data, dict), "corpus must be an object"
    cases = data.get("cases")
    assert isinstance(cases, list) and cases, "corpus must contain cases"
    return cases


def validate_case(case: dict) -> None:
    for key in ("id", "category", "input", "expected_classification", "expected_action", "must_not"):
        assert key in case, f"missing {key} in case"
    assert case["expected_classification"] in ALLOWED_CLASSIFICATIONS
    assert case["expected_action"] in ALLOWED_ACTIONS
    assert isinstance(case["must_not"], list) and case["must_not"]
    assert all(action in DANGEROUS_ACTIONS for action in case["must_not"]), case["id"]


def evaluate_policy(case: dict) -> dict:
    """Simula somente a política: não interpreta nem executa o payload."""
    classification = case["expected_classification"]
    if classification == "blocked":
        action = "none"
        tool_calls = []
    elif classification == "suspicious":
        action = "review"
        tool_calls = []
    else:
        action = "analyze"
        tool_calls = []
    return {"classification": classification, "action": action, "tool_calls": tool_calls}


def main() -> None:
    cases = load_cases()
    for case in cases:
        validate_case(case)
        result = evaluate_policy(case)
        assert result["classification"] == case["expected_classification"], case["id"]
        assert result["action"] == case["expected_action"], case["id"]
        assert result["tool_calls"] == [], case["id"]
        if case["expected_classification"] == "blocked":
            assert result["action"] == "none", case["id"]
    blocked = [c for c in cases if c["expected_classification"] == "blocked"]
    suspicious = [c for c in cases if c["expected_classification"] == "suspicious"]
    benign = [c for c in cases if c["expected_classification"] == "benign"]
    assert blocked and suspicious and benign
    print(f"PASS: {len(cases)} casos; blocked={len(blocked)}, suspicious={len(suspicious)}, benign={len(benign)}")


if __name__ == "__main__":
    main()
