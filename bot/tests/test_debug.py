"""Tests for debug module"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
import disnake
from disnake.ext import commands


@pytest.fixture
def bot():
    """Create a mock bot instance"""
    bot = Mock(spec=commands.Bot)
    bot.get_cog = Mock()
    bot.remove_cog = Mock()
    bot.load_extension = Mock()
    return bot


@pytest.fixture
def debug_cog(bot):
    """Create DebugStuff cog instance"""
    with patch('toml.load'):
        from src.exts.debug import DebugStuff
        return DebugStuff(bot)


class TestDebug:
    """Test suite for DebugStuff cog"""

    def test_cog_initialization(self, debug_cog, bot):
        """Test that DebugStuff cog initializes correctly"""
        assert debug_cog.bot == bot

    @pytest.mark.asyncio
    async def test_check_cog_exists(self, debug_cog, bot):
        """Test check_cog when cog exists"""
        inter = AsyncMock()
        inter.send = AsyncMock()
        bot.get_cog.return_value = Mock()  # Cog exists

        await debug_cog.check_cog(inter, name="TestCog")

        bot.get_cog.assert_called_once_with("TestCog")
        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "find" in call_args

    @pytest.mark.asyncio
    async def test_check_cog_not_exists(self, debug_cog, bot):
        """Test check_cog when cog doesn't exist"""
        inter = AsyncMock()
        inter.send = AsyncMock()
        bot.get_cog.return_value = None  # Cog doesn't exist

        await debug_cog.check_cog(inter, name="NonExistent")

        bot.get_cog.assert_called_once_with("NonExistent")
        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "could not find" in call_args

    @pytest.mark.asyncio
    async def test_remove_cog_success(self, debug_cog, bot):
        """Test remove_cog when successful"""
        inter = AsyncMock()
        inter.send = AsyncMock()
        bot.remove_cog.return_value = Mock()  # Success

        await debug_cog.remove_cog(inter, name="TestCog")

        bot.remove_cog.assert_called_once_with("TestCog")
        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "removed" in call_args

    @pytest.mark.asyncio
    async def test_remove_cog_failure(self, debug_cog, bot):
        """Test remove_cog when it fails"""
        inter = AsyncMock()
        inter.send = AsyncMock()
        bot.remove_cog.return_value = None  # Failure

        await debug_cog.remove_cog(inter, name="NonExistent")

        bot.remove_cog.assert_called_once_with("NonExistent")
        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "could not remove" in call_args

    @pytest.mark.asyncio
    async def test_add_cog_success(self, debug_cog, bot):
        """Test add_cog when successful"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()

        await debug_cog.add_cog(inter, name="src.exts.test")

        inter.response.defer.assert_called_once()
        bot.load_extension.assert_called_once_with("src.exts.test")
        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "loaded" in call_args

    @pytest.mark.asyncio
    async def test_add_cog_failure(self, debug_cog, bot):
        """Test add_cog when it fails"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        bot.load_extension.side_effect = Exception("Load error")

        await debug_cog.add_cog(inter, name="src.exts.invalid")

        inter.response.defer.assert_called_once()
        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "Failed" in call_args

    @pytest.mark.asyncio
    async def test_ds_command(self, debug_cog):
        """Test ds (debug shell) command"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()

        with patch('src.exts.debug.run_command_shell') as mock_run:
            mock_run.return_value = "command output"
            
            await debug_cog.ds(inter, what="ls -la")

            inter.response.defer.assert_called_once()
            mock_run.assert_called_once()
            inter.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_ds_command_long_output(self, debug_cog):
        """Test ds command with long output"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()

        with patch('src.exts.debug.run_command_shell') as mock_run, \
             patch('src.exts.debug.paste') as mock_paste:
            mock_run.return_value = "x" * 2000
            mock_paste.return_value = "http://paste.example.com"
            
            await debug_cog.ds(inter, what="cat largefile")

            mock_paste.assert_called_once()
            inter.send.assert_called_once()
