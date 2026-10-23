import check_tools


def test_parse_version():
    assert check_tools.parse_version("Bicep CLI version 0.30.3 (abc)") == (0, 30, 3)
    assert check_tools.parse_version("no digits") is None


def test_missing_tool_is_red_not_a_crash():
    assert check_tools.run(["definitely-not-a-real-tool-xyz", "--version"]) is None
    tool = check_tools.Tool("ghost", ["definitely-not-a-real-tool-xyz"])
    assert check_tools.check_tool(tool, {}) == (False, "not found")


def test_minimum_version():
    old = check_tools.Tool("Azure CLI", [], (2, 80))
    assert check_tools.check_tool(old, {"azure-cli": "2.70.0"})[0] is False
    assert check_tools.check_tool(old, {"azure-cli": "2.91.0"}) == (True, "2.91.0")
