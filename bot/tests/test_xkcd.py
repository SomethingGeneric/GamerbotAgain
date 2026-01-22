"""Tests for xkcd module"""
import pytest
from unittest.mock import Mock, AsyncMock, patch, mock_open
import disnake
from disnake.ext import commands


@pytest.fixture
def bot():
    """Create a mock bot instance"""
    bot = Mock(spec=commands.Bot)
    bot.owner_id = 123456
    bot.fetch_user = AsyncMock()
    bot.wait_until_ready = AsyncMock()
    return bot


@pytest.fixture
def mock_config():
    """Mock config for xkcd module"""
    return {'volpath': '/tmp/test_data'}


@pytest.fixture
def xkcd_cog(bot, mock_config):
    """Create xkcd cog instance"""
    with patch('toml.load', return_value=mock_config):
        with patch('os.path.exists', return_value=False):
            from src.exts.xkcd import xkcd
            cog = xkcd(bot)
            cog.data_done = True  # Skip data loading for tests
            cog.data = {
                1: {"num": 1, "safe_title": "Test Comic", "alt": "Test alt text"},
                2: {"num": 2, "safe_title": "Another Comic", "alt": "Another alt"}
            }
            return cog


class TestXkcd:
    """Test suite for xkcd cog"""

    def test_cog_initialization(self, xkcd_cog, bot):
        """Test that xkcd cog initializes correctly"""
        assert xkcd_cog.bot == bot
        assert xkcd_cog.data is not None

    @pytest.mark.asyncio
    async def test_xkcdsearch_found(self, xkcd_cog):
        """Test xkcd search when comic is found"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()

        await xkcd_cog.xkcdsearch(inter, query="Test Comic")

        inter.response.defer.assert_called_once()
        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "xkcd.com" in call_args

    @pytest.mark.asyncio
    async def test_xkcdsearch_not_found(self, xkcd_cog):
        """Test xkcd search when comic is not found"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()

        await xkcd_cog.xkcdsearch(inter, query="Nonexistent Comic")

        inter.response.defer.assert_called_once()
        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "Not found" in call_args

    @pytest.mark.asyncio
    async def test_xkcdsearch_data_not_ready(self, xkcd_cog):
        """Test xkcd search when data is not loaded"""
        xkcd_cog.data_done = False
        inter = AsyncMock()
        inter.send = AsyncMock()

        await xkcd_cog.xkcdsearch(inter, query="Test")

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "not yet loaded" in call_args

    @pytest.mark.asyncio
    async def test_xkcdsearch_by_alt_text(self, xkcd_cog):
        """Test xkcd search by alt text"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()

        await xkcd_cog.xkcdsearch(inter, query="Another alt")

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "xkcd.com/2" in call_args

    @pytest.mark.asyncio
    async def test_reset_xkcd_owner_only(self, xkcd_cog):
        """Test reset_xkcd command (owner only)"""
        inter = AsyncMock()
        inter.author.id = 123456  # Owner
        inter.send = AsyncMock()

        with patch('os.remove') as mock_remove, \
             patch.object(xkcd_cog, 'setup_data') as mock_setup:
            
            await xkcd_cog.reset_xkcd(inter)

            mock_remove.assert_called_once()
            mock_setup.assert_called_once()

    @pytest.mark.asyncio
    async def test_reset_xkcd_non_owner(self, xkcd_cog):
        """Test reset_xkcd command by non-owner"""
        inter = AsyncMock()
        inter.author.id = 999999  # Not owner
        inter.send = AsyncMock()

        await xkcd_cog.reset_xkcd(inter)

        inter.send.assert_called_once_with("nope")
