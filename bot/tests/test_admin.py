"""Tests for admin module"""
import pytest
from unittest.mock import Mock, AsyncMock
import disnake
from disnake.ext import commands


@pytest.fixture
def bot():
    """Create a mock bot instance"""
    bot = Mock(spec=commands.Bot)
    bot.user = Mock()
    bot.user.id = 123456
    bot.user.created_at = "2020-01-01"
    bot.user.display_avatar.url = "https://example.com/avatar.png"
    bot.guilds = [Mock(), Mock()]
    bot.users = [Mock() for _ in range(10)]
    bot.extensions = ["ext1", "ext2", "ext3"]
    return bot


@pytest.fixture
def admin_cog(bot):
    """Create Admin cog instance"""
    from src.exts.admin import Admin
    return Admin(bot)


class TestAdmin:
    """Test suite for Admin cog"""

    def test_cog_initialization(self, admin_cog, bot):
        """Test that Admin cog initializes correctly"""
        assert admin_cog.bot == bot

    @pytest.mark.asyncio
    async def test_botinfo_command(self, admin_cog, bot):
        """Test bot-info command"""
        inter = AsyncMock()
        inter.send = AsyncMock()
        inter.bot = bot

        await admin_cog.botinfo.callback(admin_cog, inter)

        inter.send.assert_called_once()
        call_args = inter.send.call_args
        assert 'embed' in call_args[1]
        embed = call_args[1]['embed']
        assert isinstance(embed, disnake.Embed)

    @pytest.mark.asyncio
    async def test_extensions_command(self, admin_cog, bot):
        """Test extentions command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        await admin_cog.exts.callback(admin_cog, inter)

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "ext1" in call_args
        assert "ext2" in call_args
        assert "ext3" in call_args
