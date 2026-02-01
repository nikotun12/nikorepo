import pytest
import json
from mcp_obsidian import tools
import os


@pytest.fixture
def mock_vault_basic(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    
    target = vault / "target.md"
    target.write_text("# Target Note\n\nThis is the target.")
    
    linking_note = vault / "linker.md"
    linking_note.write_text("# Linker\n\nSee [[target]] for details.")
    
    no_link_note = vault / "other.md"
    no_link_note.write_text("# Other\n\nNo links here.")
    
    return vault


@pytest.fixture
def mock_vault_complex(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    
    target = vault / "target.md"
    target.write_text("---\naliases: [goal, objective]\n---\n# Target Note")
    
    link_with_extension = vault / "note1.md"
    link_with_extension.write_text("See [[target.md]] here.")
    
    link_without_extension = vault / "note2.md"
    link_without_extension.write_text("See [[target]] here.")
    
    link_with_alias = vault / "note3.md"
    link_with_alias.write_text("See [[goal]] for info.")
    
    link_with_pipe_alias = vault / "note4.md"
    link_with_pipe_alias.write_text("See [[target|the target]] here.")
    
    multiple_links = vault / "note5.md"
    multiple_links.write_text("Both [[target]] and [[target.md]] mentioned.")
    
    no_links = vault / "note6.md"
    no_links.write_text("Just plain text.")
    
    subfolder = vault / "projects"
    subfolder.mkdir()
    
    nested_link = subfolder / "project.md"
    nested_link.write_text("Reference: [[target]]")
    
    return vault


@pytest.fixture
def mock_vault_edge_cases(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    
    target = vault / "meeting.md"
    target.write_text("# Meeting Notes")
    
    similar_name = vault / "meeting-2024.md"
    similar_name.write_text("Different file")
    
    link_to_target = vault / "agenda.md"
    link_to_target.write_text("See [[meeting]] notes.")
    
    link_to_similar = vault / "review.md"
    link_to_similar.write_text("See [[meeting-2024]] notes.")
    
    code_block_link = vault / "code.md"
    code_block_link.write_text("```\n[[meeting]] should not count\n```")
    
    inline_code_link = vault / "inline.md"
    inline_code_link.write_text("The `[[meeting]]` link is in inline code.")
    
    escaped_link = vault / "escaped.md"
    escaped_link.write_text("\\[[meeting]] is escaped.")
    
    return vault


class TestBacklinkDiscoveryBasic:
    
    def test_find_single_backlink(self, mock_vault_basic):
        tool = tools.BacklinkDiscoveryToolHandler()
        result = tool.run_tool({
            "target_path": "target.md",
            "vault_path": str(mock_vault_basic)
        })
        
        data = json.loads(result[0].text)
        assert len(data) == 1
        assert "linker.md" in data[0]["path"]
    
    def test_output_includes_path_and_filename(self, mock_vault_basic):
        tool = tools.BacklinkDiscoveryToolHandler()
        result = tool.run_tool({
            "target_path": "target.md",
            "vault_path": str(mock_vault_basic)
        })
        
        data = json.loads(result[0].text)
        assert len(data) == 1
        assert "path" in data[0]
        assert "filename" in data[0]
        assert data[0]["filename"] == "linker.md"
    
    def test_no_backlinks_returns_empty(self, mock_vault_basic):
        tool = tools.BacklinkDiscoveryToolHandler()
        result = tool.run_tool({
            "target_path": "other.md",
            "vault_path": str(mock_vault_basic)
        })
        
        data = json.loads(result[0].text)
        assert len(data) == 0
    
    def test_target_not_in_results(self, mock_vault_basic):
        tool = tools.BacklinkDiscoveryToolHandler()
        result = tool.run_tool({
            "target_path": "target.md",
            "vault_path": str(mock_vault_basic)
        })
        
        data = json.loads(result[0].text)
        for item in data:
            assert "target.md" not in item["path"]


class TestBacklinkDiscoveryFormats:
    
    def test_link_with_md_extension(self, mock_vault_complex):
        tool = tools.BacklinkDiscoveryToolHandler()
        result = tool.run_tool({
            "target_path": "target.md",
            "vault_path": str(mock_vault_complex)
        })
        
        data = json.loads(result[0].text)
        paths = [item["path"] for item in data]
        assert any("note1.md" in p for p in paths)
    
    def test_link_without_md_extension(self, mock_vault_complex):
        tool = tools.BacklinkDiscoveryToolHandler()
        result = tool.run_tool({
            "target_path": "target.md",
            "vault_path": str(mock_vault_complex)
        })
        
        data = json.loads(result[0].text)
        paths = [item["path"] for item in data]
        assert any("note2.md" in p for p in paths)
    
    def test_link_with_alias(self, mock_vault_complex):
        tool = tools.BacklinkDiscoveryToolHandler()
        result = tool.run_tool({
            "target_path": "target.md",
            "vault_path": str(mock_vault_complex)
        })
        
        data = json.loads(result[0].text)
        paths = [item["path"] for item in data]
        assert any("note3.md" in p for p in paths)
    
    def test_link_with_pipe_alias(self, mock_vault_complex):
        tool = tools.BacklinkDiscoveryToolHandler()
        result = tool.run_tool({
            "target_path": "target.md",
            "vault_path": str(mock_vault_complex)
        })
        
        data = json.loads(result[0].text)
        paths = [item["path"] for item in data]
        assert any("note4.md" in p for p in paths)
    
    def test_note_appears_once_despite_multiple_links(self, mock_vault_complex):
        tool = tools.BacklinkDiscoveryToolHandler()
        result = tool.run_tool({
            "target_path": "target.md",
            "vault_path": str(mock_vault_complex)
        })
        
        data = json.loads(result[0].text)
        paths = [item["path"] for item in data]
        note5_count = sum(1 for p in paths if "note5.md" in p)
        assert note5_count == 1
    
    def test_nested_folder_links_found(self, mock_vault_complex):
        tool = tools.BacklinkDiscoveryToolHandler()
        result = tool.run_tool({
            "target_path": "target.md",
            "vault_path": str(mock_vault_complex)
        })
        
        data = json.loads(result[0].text)
        paths = [item["path"] for item in data]
        assert any("project.md" in p for p in paths)


class TestBacklinkDiscoveryEdgeCases:
    
    def test_similar_names_not_confused(self, mock_vault_edge_cases):
        tool = tools.BacklinkDiscoveryToolHandler()
        result = tool.run_tool({
            "target_path": "meeting.md",
            "vault_path": str(mock_vault_edge_cases)
        })
        
        data = json.loads(result[0].text)
        paths = [item["path"] for item in data]
        
        assert any("agenda.md" in p for p in paths)
        assert not any("review.md" in p for p in paths)
    
    def test_code_blocks_ignored(self, mock_vault_edge_cases):
        tool = tools.BacklinkDiscoveryToolHandler()
        result = tool.run_tool({
            "target_path": "meeting.md",
            "vault_path": str(mock_vault_edge_cases)
        })
        
        data = json.loads(result[0].text)
        paths = [item["path"] for item in data]
        assert not any("code.md" in p for p in paths)
    
    def test_inline_code_blocks_ignored(self, mock_vault_edge_cases):
        tool = tools.BacklinkDiscoveryToolHandler()
        result = tool.run_tool({
            "target_path": "meeting.md",
            "vault_path": str(mock_vault_edge_cases)
        })
        
        data = json.loads(result[0].text)
        paths = [item["path"] for item in data]
        assert not any("inline.md" in p for p in paths)
    
    def test_escaped_links_ignored(self, mock_vault_edge_cases):
        tool = tools.BacklinkDiscoveryToolHandler()
        result = tool.run_tool({
            "target_path": "meeting.md",
            "vault_path": str(mock_vault_edge_cases)
        })
        
        data = json.loads(result[0].text)
        paths = [item["path"] for item in data]
        assert not any("escaped.md" in p for p in paths)


class TestBacklinkDiscoveryErrors:
    
    def test_nonexistent_target(self, mock_vault_basic):
        tool = tools.BacklinkDiscoveryToolHandler()
        
        with pytest.raises(Exception):
            tool.run_tool({
                "target_path": "nonexistent.md",
                "vault_path": str(mock_vault_basic)
            })
    
    def test_missing_target_path_argument(self, mock_vault_basic):
        tool = tools.BacklinkDiscoveryToolHandler()
        
        with pytest.raises(Exception):
            tool.run_tool({
                "vault_path": str(mock_vault_basic)
            })
    
    def test_invalid_vault_path(self):
        tool = tools.BacklinkDiscoveryToolHandler()
        
        with pytest.raises(Exception):
            tool.run_tool({
                "target_path": "target.md",
                "vault_path": "/nonexistent/vault"
            })


class TestBacklinkDiscoveryToolRegistration:
    
    def test_tool_handler_exists(self):
        assert hasattr(tools, 'BacklinkDiscoveryToolHandler')
    
    def test_tool_has_correct_name(self):
        tool = tools.BacklinkDiscoveryToolHandler()
        assert tool.name == "obsidian_get_backlinks"
    
    def test_tool_description_exists(self):
        tool = tools.BacklinkDiscoveryToolHandler()
        description = tool.get_tool_description()
        assert description.name == "obsidian_get_backlinks"
        assert len(description.description) > 0
    
    def test_tool_schema_has_target_path(self):
        tool = tools.BacklinkDiscoveryToolHandler()
        description = tool.get_tool_description()
        assert "target_path" in description.inputSchema["properties"]
        assert "target_path" in description.inputSchema["required"]
    
    def test_tool_registered_in_server(self):
        from mcp_obsidian import server
        registered_tool_names = [name for name in server.tool_handlers.keys()]
        assert "obsidian_get_backlinks" in registered_tool_names

