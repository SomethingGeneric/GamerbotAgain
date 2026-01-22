"""Tests for randomstuff module"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
import disnake
from disnake.ext import commands


@pytest.fixture
def bot():
    """Create a mock bot instance"""
    return Mock(spec=commands.Bot)


@pytest.fixture
def random_cog(bot):
    """Create RandomThings cog instance"""
    with patch('toml.load'):
        from src.exts.randomstuff import RandomThings
        return RandomThings(bot)


class TestRandomStuff:
    """Test suite for RandomThings cog"""

    def test_cog_initialization(self, random_cog, bot):
        """Test that RandomThings cog initializes correctly"""
        assert random_cog.bot == bot

    @pytest.mark.asyncio
    async def test_ping_command(self, random_cog):
        """Test ping command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        with patch('disnake.File') as mock_file:
            await random_cog.ping(inter)

            inter.send.assert_called_once()
            call_args = inter.send.call_args[0][0]
            assert "pong" in call_args

    @pytest.mark.asyncio
    async def test_gcache_command(self, random_cog):
        """Test gcache command"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        await random_cog.gcache(inter, url="https://example.com")

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "cache:" in call_args
        assert "example.com" in call_args

    @pytest.mark.asyncio
    async def test_math_command(self, random_cog):
        """Test math command with simple expression"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        with patch('src.exts.randomstuff.run_command_shell') as mock_run:
            mock_run.return_value = "42"
            
            await random_cog.math(inter, exp="6*7")

            mock_run.assert_called_once()
            inter.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_math_command_no_output(self, random_cog):
        """Test math command with no output"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        with patch('src.exts.randomstuff.run_command_shell') as mock_run:
            mock_run.return_value = ""
            
            await random_cog.math(inter, exp="invalid")

            inter.send.assert_called_once()
            # Should send warning about no output

    @pytest.mark.asyncio
    async def test_math_command_long_output(self, random_cog):
        """Test math command with long output"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        with patch('src.exts.randomstuff.run_command_shell') as mock_run, \
             patch('src.exts.randomstuff.paste') as mock_paste:
            mock_run.return_value = "x" * 2000
            mock_paste.return_value = "http://paste.example.com"
            
            await random_cog.math(inter, exp="2^1000")

            mock_paste.assert_called_once()
            inter.send.assert_called_once()


# NOTES ON MODULE ORGANIZATION:
# - The gcache command seems like it could belong in the internet module
#   since it's a web-related tool, not random stuff
# - The math command could arguably be in a utilities or tools module
