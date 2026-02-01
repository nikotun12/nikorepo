import pytest
from mcp_obsidian import tools


class TestExistingToolsUnaffected:
    
    def test_list_files_in_vault_still_exists(self):
        assert hasattr(tools, 'ListFilesInVaultToolHandler')
        tool = tools.ListFilesInVaultToolHandler()
        assert tool.name == "obsidian_list_files_in_vault"
    
    def test_get_file_contents_still_exists(self):
        assert hasattr(tools, 'GetFileContentsToolHandler')
        tool = tools.GetFileContentsToolHandler()
        assert tool.name == "obsidian_get_file_contents"
    
    def test_search_tool_still_exists(self):
        assert hasattr(tools, 'SearchToolHandler')
        tool = tools.SearchToolHandler()
        assert tool.name == "obsidian_simple_search"
    
    def test_patch_content_still_exists(self):
        assert hasattr(tools, 'PatchContentToolHandler')
        tool = tools.PatchContentToolHandler()
        assert tool.name == "obsidian_patch_content"
    
    def test_append_content_still_exists(self):
        assert hasattr(tools, 'AppendContentToolHandler')
        tool = tools.AppendContentToolHandler()
        assert tool.name == "obsidian_append_content"
    
    def test_delete_file_still_exists(self):
        assert hasattr(tools, 'DeleteFileToolHandler')
        tool = tools.DeleteFileToolHandler()
        assert tool.name == "obsidian_delete_file"
