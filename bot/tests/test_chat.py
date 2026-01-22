"""Tests for chat module"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
import disnake
from disnake.ext import commands


@pytest.fixture
def bot():
    """Create a mock bot instance"""
    return Mock(spec=commands.Bot)


@pytest.fixture
def chat_cog(bot):
    """Create Chat cog instance"""
    with patch('toml.load'):
        from src.exts.chat import Chat
        return Chat(bot)


class TestChat:
    """Test suite for Chat cog"""

    def test_cog_initialization(self, chat_cog, bot):
        """Test that Chat cog initializes correctly"""
        assert chat_cog.bot == bot

    @pytest.mark.asyncio
    async def test_crab_command(self, chat_cog):
        """Test crab command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        await chat_cog.crab.callback(chat_cog, inter)

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "tenor.com" in call_args

    @pytest.mark.asyncio
    async def test_deadchat_command(self, chat_cog):
        """Test deadchat command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        await chat_cog.deadchat.callback(chat_cog, inter)

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "tenor.com" in call_args

    @pytest.mark.asyncio
    async def test_xd_command(self, chat_cog):
        """Test xd command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        with patch('disnake.File') as mock_file:
            await chat_cog.xd.callback(chat_cog, inter)

            inter.send.assert_called_once()
            mock_file.assert_called_with("images/LMAO.jpg")

    @pytest.mark.asyncio
    async def test_kat_command(self, chat_cog):
        """Test kat command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        with patch('disnake.File') as mock_file:
            await chat_cog.kat.callback(chat_cog, inter)

            inter.send.assert_called_once()
            mock_file.assert_called_with("images/krying_kat.png")

    @pytest.mark.asyncio
    async def test_yea_command(self, chat_cog):
        """Test yea command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        with patch('disnake.File') as mock_file:
            await chat_cog.yea.callback(chat_cog, inter)

            inter.send.assert_called_once()
            mock_file.assert_called_with("images/yeah.png")

    @pytest.mark.asyncio
    async def test_no_command(self, chat_cog):
        """Test no command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        with patch('disnake.File') as mock_file:
            await chat_cog.no.callback(chat_cog, inter)

            inter.send.assert_called_once()
            mock_file.assert_called_with("images/no.png")
