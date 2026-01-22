"""Tests for schizo module"""
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
def schizo_cog(bot):
    """Create Schizo cog instance"""
    with patch('toml.load', return_value={}):
        with patch('builtins.open', mock_open(read_data='message1\nmessage2\nmessage3')):
            with patch('disnake.ext.tasks.loop'):
                from src.exts.schizo import Schizo
                cog = Schizo(bot)
                # Mock the task to prevent it from running
                cog.schizo_task = Mock()
                cog.schizo_task.start = Mock()
                return cog


class TestSchizo:
    """Test suite for Schizo cog"""

    def test_cog_initialization(self, schizo_cog, bot):
        """Test that Schizo cog initializes correctly"""
        assert schizo_cog.bot == bot
        assert len(schizo_cog.unhinged) > 0

    @pytest.mark.asyncio
    async def test_be_silly(self, schizo_cog, bot):
        """Test be_silly method"""
        mock_user = AsyncMock()
        bot.fetch_user.return_value = mock_user

        await schizo_cog.be_silly()

        bot.fetch_user.assert_called_once_with(721355984940957816)
        mock_user.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_be_silly_error(self, schizo_cog, bot):
        """Test be_silly with error"""
        bot.fetch_user.side_effect = Exception("User not found")

        # Should not raise exception
        await schizo_cog.be_silly()

    @pytest.mark.asyncio
    async def test_dm_command_owner(self, schizo_cog, bot):
        """Test dm command as owner"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 123456  # Owner
        inter.bot = bot

        mock_user = AsyncMock()
        bot.fetch_user.return_value = mock_user

        await schizo_cog.dm.callback(schizo_cog, inter, text="<@!999999>Hello there")

        inter.response.defer.assert_called_once()
        bot.fetch_user.assert_called_once_with(999999)
        mock_user.send.assert_called_once_with("Hello there")

    @pytest.mark.asyncio
    async def test_dm_command_non_owner(self, schizo_cog):
        """Test dm command as non-owner"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 999999  # Not owner

        await schizo_cog.dm.callback(schizo_cog, inter, text="<@!123456>Test")

        inter.send.assert_called_once_with("You can't do that!")

    def test_make_bonk(self, schizo_cog):
        """Test make_bonk method"""
        with patch('PIL.Image.open') as mock_open, \
             patch('PIL.ImageDraw.Draw') as mock_draw, \
             patch('PIL.ImageFont.truetype') as mock_font:
            
            mock_img = Mock()
            mock_img.save = Mock()
            mock_open.return_value = mock_img

            schizo_cog.make_bonk("test")

            mock_img.save.assert_called_once_with("bonk-s.png")

    @pytest.mark.asyncio
    async def test_on_ready(self, schizo_cog):
        """Test on_ready event"""
        with patch.object(schizo_cog, 'be_silly') as mock_be_silly:
            await schizo_cog.on_ready()

            mock_be_silly.assert_called_once()


# NOTES ON MODULE ORGANIZATION:
# - The schizo module contains bot automation tasks and owner utilities
# - The make_bonk method seems like it should be in the imgmaker module
#   since it's image manipulation functionality
# - This module is a bit of a catch-all for various bot behaviors
