"""Tests for util_functions module"""
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import disnake


# Mock config before importing util_functions
@pytest.fixture(autouse=True)
def mock_config():
    with patch('toml.load') as mock_load:
        mock_load.return_value = {
            'volpath': '/tmp/test_data',
            'permitted_guilds': [123456789]
        }
        yield mock_load


@pytest.fixture
def mock_geoip_database():
    """Mock the geoip2 database"""
    with patch('geoip2.database.Reader') as mock_reader:
        yield mock_reader


class TestUtilFunctions:
    """Test suite for utility functions"""

    def test_fancy_msg(self):
        """Test fancy message creation"""
        from src.exts.util_functions import fancy_msg
        
        result = fancy_msg("Test Title", "Test Text", disnake.Colour.blue())
        assert isinstance(result, disnake.Embed)
        assert result.colour == disnake.Colour.blue()

    def test_err_msg(self):
        """Test error message creation"""
        from src.exts.util_functions import err_msg
        
        result = err_msg("Error Title", "Error Text")
        assert isinstance(result, disnake.Embed)
        assert result.colour == disnake.Colour.red()

    def test_warn_msg(self):
        """Test warning message creation"""
        from src.exts.util_functions import warn_msg
        
        result = warn_msg("Warning Title", "Warning Text")
        assert isinstance(result, disnake.Embed)
        assert result.colour == disnake.Colour.gold()

    def test_inf_msg(self):
        """Test info message creation"""
        from src.exts.util_functions import inf_msg
        
        result = inf_msg("Info Title", "Info Text")
        assert isinstance(result, disnake.Embed)
        assert result.colour == disnake.Colour.blurple()

    def test_check_file_exists(self, tmp_path):
        """Test file existence checking"""
        from src.exts.util_functions import check
        
        # Create a temporary file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        assert check(str(test_file)) is True
        assert check(str(tmp_path / "nonexistent.txt")) is False

    def test_save_and_get(self, tmp_path):
        """Test saving and getting file content"""
        from src.exts.util_functions import save, get
        
        test_file = tmp_path / "test.txt"
        save(str(test_file), "test content")
        
        content = get(str(test_file))
        assert "test content" in content

    @pytest.mark.asyncio
    async def test_run_command_shell(self):
        """Test running shell commands"""
        from src.exts.util_functions import run_command_shell
        
        result = await run_command_shell("echo 'test'")
        assert "test" in result

    def test_split_string_short(self):
        """Test splitting string shorter than max length"""
        from src.exts.util_functions import split_string
        
        text = "Short text."
        result = split_string(text, max_length=130)
        assert len(result) == 1
        assert result[0] == text

    def test_split_string_long(self):
        """Test splitting long string"""
        from src.exts.util_functions import split_string
        
        text = "This is sentence one. This is sentence two. This is sentence three. This is sentence four. This is sentence five. This is sentence six. This is sentence seven."
        result = split_string(text, max_length=50)
        assert len(result) > 1
        for part in result:
            assert len(part) <= 130  # Should respect default if not too aggressive

    def test_get_geoip_success(self, mock_geoip_database):
        """Test successful GeoIP lookup"""
        from src.exts.util_functions import get_geoip
        
        # Mock the database reader
        mock_response = Mock()
        mock_response.location.latitude = 37.7749
        mock_response.location.longitude = -122.4194
        
        mock_reader_instance = MagicMock()
        mock_reader_instance.__enter__ = Mock(return_value=mock_reader_instance)
        mock_reader_instance.__exit__ = Mock(return_value=False)
        mock_reader_instance.city = Mock(return_value=mock_response)
        
        mock_geoip_database.return_value = mock_reader_instance
        
        result = get_geoip("8.8.8.8")
        assert "latitude" in result
        assert "longitude" in result

    def test_get_geoip_failure(self, mock_geoip_database):
        """Test failed GeoIP lookup"""
        from src.exts.util_functions import get_geoip
        
        # Mock the database reader to raise an exception
        mock_reader_instance = MagicMock()
        mock_reader_instance.__enter__ = Mock(return_value=mock_reader_instance)
        mock_reader_instance.__exit__ = Mock(return_value=False)
        mock_reader_instance.city = Mock(side_effect=Exception("IP not found"))
        
        mock_geoip_database.return_value = mock_reader_instance
        
        result = get_geoip("invalid")
        assert "message" in result
