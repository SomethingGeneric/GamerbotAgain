"""Tests for fuckedup module"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
import disnake
from disnake.ext import commands


@pytest.fixture
def bot():
    """Create a mock bot instance"""
    return Mock(spec=commands.Bot)


@pytest.fixture
def fuckedup_cog(bot):
    """Create FuckedUpStuff cog instance"""
    from src.exts.fuckedup import FuckedUpStuff
    return FuckedUpStuff(bot)


class TestFuckedUp:
    """Test suite for FuckedUpStuff cog"""

    def test_cog_initialization(self, fuckedup_cog, bot):
        """Test that FuckedUpStuff cog initializes correctly"""
        assert fuckedup_cog.bot == bot

    @pytest.mark.asyncio
    async def test_forgor_command(self, fuckedup_cog):
        """Test forgor command"""
        inter = AsyncMock()
        inter.message.delete = AsyncMock()
        inter.send = AsyncMock()

        await fuckedup_cog.forgor(inter)

        # Message deletion should be attempted
        inter.message.delete.assert_called_once()
        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "tenor.com" in call_args

    @pytest.mark.asyncio
    async def test_forgor_command_no_delete_perms(self, fuckedup_cog):
        """Test forgor command when bot can't delete message"""
        inter = AsyncMock()
        inter.message.delete = AsyncMock(side_effect=Exception("No perms"))
        inter.send = AsyncMock()

        await fuckedup_cog.forgor(inter)

        # Should still send the GIF even if delete fails
        inter.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_elb_command(self, fuckedup_cog):
        """Test elb command"""
        inter = AsyncMock()
        inter.message.delete = AsyncMock()
        inter.send = AsyncMock()

        await fuckedup_cog.elb(inter)

        inter.message.delete.assert_called_once()
        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "tenor.com" in call_args

    @pytest.mark.asyncio
    async def test_facepalm_command(self, fuckedup_cog):
        """Test facepalm command"""
        inter = AsyncMock()
        inter.message.delete = AsyncMock()
        inter.send = AsyncMock()

        await fuckedup_cog.facepalm(inter)

        inter.message.delete.assert_called_once()
        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "tenor.com" in call_args


# NOTES ON MODULE ORGANIZATION:
# - This module contains meme/reaction commands
# - Could potentially be merged with chat module as they serve similar purposes
# - The name "fuckedup" is somewhat ambiguous for the functionality
