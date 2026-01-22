"""Tests for about module"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
import disnake
from disnake.ext import commands


@pytest.fixture
def bot():
    """Create a mock bot instance"""
    return Mock(spec=commands.Bot)


@pytest.fixture
def about_cog(bot):
    """Create About cog instance"""
    with patch('toml.load'):
        from src.exts.about import About
        return About(bot)


class TestAbout:
    """Test suite for About cog"""

    def test_cog_initialization(self, about_cog, bot):
        """Test that About cog initializes correctly"""
        assert about_cog.bot == bot

    @pytest.mark.asyncio
    async def test_source_command(self, about_cog):
        """Test source command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        await about_cog.source.callback(about_cog, inter)

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "source code" in call_args.lower()
        assert "git.goober.cloud" in call_args

    @pytest.mark.asyncio
    async def test_license_command(self, about_cog):
        """Test license command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        await about_cog.license.callback(about_cog, inter)

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "license" in call_args.lower()
        assert "git.goober.cloud" in call_args

    @pytest.mark.asyncio
    async def test_report_command(self, about_cog):
        """Test report command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        await about_cog.report.callback(about_cog, inter)

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "issues" in call_args.lower()

    @pytest.mark.asyncio
    async def test_invite_command(self, about_cog):
        """Test invite command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        await about_cog.invite.callback(about_cog, inter)

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "discord.com" in call_args
        assert "oauth2/authorize" in call_args

    @pytest.mark.asyncio
    async def test_support_command(self, about_cog):
        """Test support command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        await about_cog.support.callback(about_cog, inter)

        # Should send two arguments
        assert inter.send.call_count == 1
