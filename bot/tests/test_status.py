"""Tests for status module"""
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import disnake
from disnake.ext import commands
import datetime


@pytest.fixture
def bot():
    """Create a mock bot instance"""
    bot = Mock(spec=commands.Bot)
    bot.guilds = [Mock(), Mock()]
    for guild in bot.guilds:
        guild.member_count = 50
    bot.change_presence = AsyncMock()
    bot.wait_until_ready = AsyncMock()
    return bot


@pytest.fixture
def mock_config():
    """Mock config for status module"""
    return {
        'status_messages': ['Playing game 1', 'Playing game 2', 'with {number_users} users'],
        'status_interval': 60
    }


@pytest.fixture
def status_cog(bot, mock_config):
    """Create Status cog instance"""
    with patch('toml.load', return_value=mock_config):
        with patch('disnake.ext.tasks.loop'):
            from src.exts.status import Status
            cog = Status(bot)
            # Mock the tasks to prevent them from actually starting
            cog.status_task = Mock()
            cog.status_task.start = Mock()
            cog.uptime_logger = Mock()
            cog.uptime_logger.start = Mock()
            return cog


class TestStatus:
    """Test suite for Status cog"""

    def test_cog_initialization(self, status_cog, bot):
        """Test that Status cog initializes correctly"""
        assert status_cog.bot == bot
        assert len(status_cog.status_messages) == 3
        assert status_cog.status_interval == 60

    @pytest.mark.asyncio
    async def test_set_default_status(self, status_cog, bot):
        """Test setting default status"""
        with patch('asyncio.sleep'):
            await status_cog.set_default_status()

            bot.change_presence.assert_called_once()
            call_args = bot.change_presence.call_args
            assert 'activity' in call_args[1]

    @pytest.mark.asyncio
    async def test_set_default_status_with_user_count(self, status_cog, bot):
        """Test status message with user count placeholder"""
        status_cog.status_messages = ['with {number_users} users']
        
        with patch('asyncio.sleep'):
            await status_cog.set_default_status()

            bot.change_presence.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_uptime_command(self, status_cog):
        """Test getuptime command"""
        inter = AsyncMock()
        inter.send = AsyncMock()
        status_cog.upt = 3661  # 1 hour, 1 minute, 1 second

        await status_cog.get_uptime.callback(status_cog, inter)

        inter.send.assert_called_once()
        # Check that embed was sent
        call_args = inter.send.call_args
        assert 'embed' in call_args[1]

    @pytest.mark.asyncio
    async def test_on_ready(self, status_cog):
        """Test on_ready event"""
        with patch.object(status_cog, 'set_default_status') as mock_set_status:
            await status_cog.on_ready()

            mock_set_status.assert_called_once()
