from classicmac_mcp.compatibility import scan_c89, validation_ladder


def test_clean_c89_snippet_passes_policy_scan():
    source = """int add(int a, int b)\n{\n    int result;\n    result = a + b;\n    return result;\n}\n"""
    result = scan_c89(source)
    assert result.passed is True
    assert result.findings == []


def test_c99_for_declaration_is_rejected():
    source = """void f(void)\n{\n    int sum;\n    sum = 0;\n    for (int i = 0; i < 3; i++) sum += i;\n}\n"""
    result = scan_c89(source)
    assert result.passed is False
    assert any(item.rule_id == "c89.for-init-declaration" for item in result.findings)


def test_cpp_comment_is_rejected_by_strict_profile():
    result = scan_c89("int x; // target note\n")
    assert result.passed is False
    assert any(item.rule_id == "c89.cpp-comment" for item in result.findings)


def test_validation_ladder_keeps_retro68_non_authoritative():
    ladder = validation_ladder()
    retro = next(item for item in ladder if item["level"] == "retro68_verified")
    cw = next(item for item in ladder if item["level"] == "codewarrior_verified")
    assert "CodeWarrior" in retro["does_not_prove"]
    assert "authoritative" in cw["authority"]
