"""Tests for reminders module"""
import pytest
from unittest.mock import Mock, AsyncMock, patch, mock_open
import disnake
from disnake.ext import commands
from datetime import datetime
import pytz


@pytest.fixture
def bot():
    """Create a mock bot instance"""
    bot = Mock(spec=commands.Bot)
    bot.fetch_user = AsyncMock()
    bot.wait_until_ready = AsyncMock()
    bot.tzdata = {}
    return bot


@pytest.fixture
def mock_config():
    """Mock config for reminders module"""
    return {'volpath': '/tmp/test_data'}


@pytest.fixture
def reminders_cog(bot, mock_config):
    """Create reminders cog instance"""
    with patch('toml.load', return_value=mock_config):
        with patch('os.path.exists', return_value=False):
            with patch('disnake.ext.tasks.loop'):
                from src.exts.reminders import reminders
                cog = reminders(bot)
                cog.data = []
                cog.tzdata = {}
                # Mock the task to prevent it from running
                cog.iterate_reminders = Mock()
                cog.iterate_reminders.start = Mock()
                return cog


class TestReminders:
    """Test suite for reminders cog"""

    def test_cog_initialization(self, reminders_cog, bot):
        """Test that reminders cog initializes correctly"""
        assert reminders_cog.bot == bot
        assert isinstance(reminders_cog.data, list)

    @pytest.mark.asyncio
    async def test_show_time_no_timezone(self, reminders_cog):
        """Test show_time command without user timezone"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 123456

        await reminders_cog.show_time.callback(reminders_cog, inter)

        inter.response.defer.assert_called_once()
        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "currently" in call_args

    @pytest.mark.asyncio
    async def test_show_time_with_timezone(self, reminders_cog):
        """Test show_time command with user timezone"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 123456
        reminders_cog.tzdata[123456] = "America/New_York"

        await reminders_cog.show_time.callback(reminders_cog, inter)

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "for you" in call_args

    @pytest.mark.asyncio
    async def test_time_for_user_with_timezone(self, reminders_cog):
        """Test time_for command"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        
        user = Mock()
        user.id = 654321
        user.mention = "@testuser"
        
        reminders_cog.tzdata[654321] = "America/Los_Angeles"

        await reminders_cog.time_for.callback(reminders_cog, inter, user)

        inter.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_time_for_user_without_timezone(self, reminders_cog):
        """Test time_for command for user without timezone"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        
        user = Mock()
        user.id = 654321
        user.mention = "@testuser"

        await reminders_cog.time_for.callback(reminders_cog, inter, user)

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "hasn't used" in call_args

    @pytest.mark.asyncio
    async def test_mytz_valid_timezone(self, reminders_cog, bot):
        """Test mytz command with valid timezone"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 123456

        with patch.object(reminders_cog, 'write_data'):
            await reminders_cog.mytz.callback(reminders_cog, inter, timez="America/New_York")

            inter.send.assert_called_once_with("Noted!")
            assert bot.tzdata[123456] == "America/New_York"

    @pytest.mark.asyncio
    async def test_mytz_invalid_timezone(self, reminders_cog):
        """Test mytz command with invalid timezone"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 123456

        await reminders_cog.mytz.callback(reminders_cog, inter, timez="Invalid/Timezone")

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "doesn't seem to be a timezone" in call_args

    @pytest.mark.asyncio
    async def test_remind_without_timezone(self, reminders_cog):
        """Test remind command without user timezone set"""
        inter = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 123456

        await reminders_cog.remind.callback(reminders_cog, inter, what="Test reminder", when="2025-01-01 12:00", utc=False)

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "mytz" in call_args

    @pytest.mark.asyncio
    async def test_remind_with_utc(self, reminders_cog):
        """Test remind command with UTC"""
        inter = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 123456

        with patch.object(reminders_cog, 'write_data'):
            await reminders_cog.remind.callback(reminders_cog, inter, what="Test reminder", when="2025-01-01 12:00", utc=True)

            inter.send.assert_called_once()
            assert len(reminders_cog.data) == 1

    @pytest.mark.asyncio
    async def test_show_reminders_with_data(self, reminders_cog):
        """Test show_reminders command with existing reminders"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 123456

        reminders_cog.data = [
            {"user": 123456, "text": "Test reminder", "when": "2025-01-01 12:00", "utc": True}
        ]

        await reminders_cog.show_reminders.callback(reminders_cog, inter)

        inter.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_show_reminders_empty(self, reminders_cog):
        """Test show_reminders command with no reminders"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 123456

        reminders_cog.data = []

        await reminders_cog.show_reminders.callback(reminders_cog, inter)

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "no reminders" in call_args

    @pytest.mark.asyncio
    async def test_cancel_reminder(self, reminders_cog):
        """Test cancel_reminder command"""
        inter = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 123456

        reminders_cog.data = [
            {"user": 123456, "text": "Test reminder", "when": "2025-01-01 12:00", "utc": True}
        ]

        with patch.object(reminders_cog, 'write_data'):
            await reminders_cog.cancel_reminder.callback(reminders_cog, inter, event_id=0)

            inter.send.assert_called_once()
            assert len(reminders_cog.data) == 0
