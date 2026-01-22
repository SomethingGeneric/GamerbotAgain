"""Tests for speak module (TTS/Voice)"""
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import disnake
from disnake.ext import commands


@pytest.fixture
def bot():
    """Create a mock bot instance"""
    bot = Mock(spec=commands.Bot)
    bot.wait_until_ready = AsyncMock()
    return bot


@pytest.fixture
def speak_cog(bot):
    """Create Speak cog instance"""
    with patch('toml.load'):
        with patch('os.path.exists', return_value=False):
            from src.exts.speak import Speak
            cog = Speak(bot)
            return cog


class TestSpeak:
    """Test suite for Speak cog (TTS/Voice)"""

    def test_cog_initialization(self, speak_cog, bot):
        """Test that Speak cog initializes correctly"""
        assert speak_cog.bot == bot
        assert speak_cog.voice_client is None
        assert speak_cog.isDone is False

    @pytest.mark.asyncio
    async def test_tts_command_not_in_voice(self, speak_cog):
        """Test TTS command when user is not in voice channel"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.display_name = "TestUser"
        inter.author.voice = None
        inter.guild = Mock(spec=disnake.Guild)

        await speak_cog.tts(inter, thing="test message", stealth=False)

        inter.response.defer.assert_called_once()
        # Should send error about not being in voice channel

    @pytest.mark.asyncio
    async def test_meow_command(self, speak_cog):
        """Test meow command"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.voice = None
        inter.guild = Mock(spec=disnake.Guild)

        with patch('os.listdir', return_value=['meow1.mp3', 'meow2.mp3']):
            await speak_cog.meow(inter)

            inter.response.defer.assert_called_once()
            inter.send.assert_called_once_with("Meow")

    def test_set_done(self, speak_cog):
        """Test set_done method"""
        speak_cog.isDone = False
        speak_cog.set_done()
        assert speak_cog.isDone is True

    @pytest.mark.asyncio
    async def test_speak_in_channel_not_guild(self, speak_cog):
        """Test speak_in_channel when not in a guild"""
        inter = AsyncMock()
        inter.guild = None

        result = await speak_cog.speak_in_channel(inter, text="test")

        assert result is None

    @pytest.mark.asyncio
    async def test_speak_in_channel_voice_busy(self, speak_cog):
        """Test speak_in_channel when voice is busy"""
        inter = AsyncMock()
        inter.send = AsyncMock()
        inter.guild = Mock(spec=disnake.Guild)
        speak_cog.voice_client = Mock()  # Voice is busy

        await speak_cog.speak_in_channel(inter, text="test")

        inter.send.assert_called_once()
        # Should send error about being busy


# NOTES ON MODULE ORGANIZATION:
# - The speak module is appropriately categorized for TTS/voice features
# - All commands relate to voice channel functionality
