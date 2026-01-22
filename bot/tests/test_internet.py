"""Tests for internet module (Network/Internet Tools)"""
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import disnake
from disnake.ext import commands
import json


@pytest.fixture
def bot():
    """Create a mock bot instance"""
    return Mock(spec=commands.Bot)


@pytest.fixture
def internet_cog(bot):
    """Create InternetStuff cog instance"""
    with patch('toml.load'):
        from src.exts.internet import InternetStuff
        return InternetStuff(bot)


class TestInternetStuff:
    """Test suite for InternetStuff cog (Network/Internet Tools)"""

    def test_cog_initialization(self, internet_cog, bot):
        """Test that InternetStuff cog initializes correctly"""
        assert internet_cog.bot == bot

    @pytest.mark.asyncio
    async def test_get_as_json_success(self):
        """Test successful JSON retrieval"""
        from src.exts.internet import get_as_json
        
        with patch('src.exts.internet.run_command_shell') as mock_run:
            mock_run.return_value = '{"key": "value"}'
            result = await get_as_json("http://example.com")
            assert result == {"key": "value"}

    @pytest.mark.asyncio
    async def test_get_as_json_failure(self):
        """Test JSON retrieval error handling"""
        from src.exts.internet import get_as_json
        
        with patch('src.exts.internet.run_command_shell') as mock_run:
            mock_run.side_effect = Exception("Network error")
            result = await get_as_json("http://example.com")
            assert result == '{"haha":"heeho"}'

    @pytest.mark.asyncio
    async def test_tldr_command(self, internet_cog):
        """Test tldr command"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()

        with patch('src.exts.internet.run_command_shell') as mock_run:
            mock_run.return_value = "# tldr output\nSome documentation"
            
            await internet_cog.tldr(inter, query="ls")

            inter.response.defer.assert_called_once()
            inter.send.assert_called_once()
            call_args = inter.send.call_args[0][0]
            assert "tldr output" in call_args

    @pytest.mark.asyncio
    async def test_tldr_long_output(self, internet_cog):
        """Test tldr command with long output"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()

        with patch('src.exts.internet.run_command_shell') as mock_run, \
             patch('src.exts.internet.paste') as mock_paste:
            mock_run.return_value = "x" * 2000
            mock_paste.return_value = "http://paste.example.com"
            
            await internet_cog.tldr(inter, query="ls")

            mock_paste.assert_called_once()
            inter.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_chtsh_command(self, internet_cog):
        """Test cht.sh command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        await internet_cog.chtsh(inter, query="python list")

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "cht.sh" in call_args
        assert "python" in call_args

    @pytest.mark.asyncio
    async def test_archwiki_command(self, internet_cog):
        """Test archwiki command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        await internet_cog.archwiki(inter, query="systemd")

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "wiki.archlinux.org" in call_args
        assert "systemd" in call_args

    @pytest.mark.asyncio
    async def test_kernel_command_success(self, internet_cog):
        """Test kernel command"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()

        with patch('src.exts.internet.get_as_json') as mock_json, \
             patch('src.exts.internet.run_command_shell') as mock_run:
            mock_json.return_value = {"latest_stable": {"version": "6.6.1"}}
            mock_run.return_value = "5.15.0-generic"
            
            await internet_cog.kernel(inter)

            inter.response.defer.assert_called_once()
            inter.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_command(self, internet_cog):
        """Test search command"""
        inter = AsyncMock()
        inter.typing = MagicMock()
        inter.send = AsyncMock()

        await internet_cog.search(inter, query="python tutorial")

        inter.send.assert_called_once()
        call_args = inter.send.call_args
        assert call_args is not None

    @pytest.mark.asyncio
    async def test_traceroute_valid_url(self, internet_cog):
        """Test traceroute with valid URL"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.mention = "@user"

        with patch('src.exts.internet.run_command_shell') as mock_run:
            mock_run.return_value = "traceroute output"
            
            await internet_cog.traceroute(inter, url="example.com")

            inter.response.defer.assert_called_once()
            mock_run.assert_called_once()
            inter.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_traceroute_invalid_url(self, internet_cog):
        """Test traceroute with invalid URL"""
        inter = AsyncMock()
        inter.send = AsyncMock()
        inter.author.mention = "@user"

        await internet_cog.traceroute(inter, url="notaurl")

        inter.send.assert_called_once()
        # Should send error about invalid address

    @pytest.mark.asyncio
    async def test_whois_valid_domain(self, internet_cog):
        """Test whois with valid domain"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.mention = "@user"

        with patch('src.exts.internet.run_command_shell') as mock_run:
            mock_run.return_value = "whois data"
            
            await internet_cog.whois(inter, url="example.com")

            inter.response.defer.assert_called_once()
            mock_run.assert_called_once()
            inter.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_nmap_command(self, internet_cog):
        """Test nmap command"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.mention = "@user"

        with patch('src.exts.internet.run_command_shell') as mock_run:
            mock_run.return_value = "nmap scan results"
            
            await internet_cog.nmap(inter, url="example.com")

            inter.response.defer.assert_called_once()
            mock_run.assert_called_once()
            inter.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_geoip_command(self, internet_cog):
        """Test geoip command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        with patch('src.exts.internet.get_geoip') as mock_geoip:
            mock_geoip.return_value = {
                "latitude": 37.7749,
                "longitude": -122.4194
            }
            
            await internet_cog.geoip(inter, ip="8.8.8.8")

            mock_geoip.assert_called_once_with("8.8.8.8")
            inter.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_translate_command(self, internet_cog):
        """Test translate command"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        
        mock_message = Mock()
        mock_message.content = "Hola mundo"

        with patch('translators.translate_text') as mock_translate:
            mock_translate.return_value = "Hello world"
            
            await internet_cog.trns(inter, mock_message)

            inter.response.defer.assert_called_once()
            mock_translate.assert_called_once_with("Hola mundo")
            inter.send.assert_called_once()


# NOTES ON MODULE ORGANIZATION:
# - The internet module seems well-organized for network/internet tools
# - All commands are appropriately categorized under "Internet-ish tools"
