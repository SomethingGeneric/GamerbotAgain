"""Tests for shell module (Linux/Shell Commands)"""
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock, mock_open
import disnake
from disnake.ext import commands


@pytest.fixture
def bot():
    """Create a mock bot instance"""
    return Mock(spec=commands.Bot)


@pytest.fixture
def mock_config():
    """Mock config for shell module"""
    return {
        'volpath': '/tmp/test_data',
        'permitted_guilds': [123456789]
    }


@pytest.fixture
def shell_cog(bot, mock_config):
    """Create Shell cog instance"""
    with patch('toml.load', return_value=mock_config):
        with patch('os.path.exists', return_value=False):
            from src.exts.shell import Shell
            return Shell(bot)


class TestShell:
    """Test suite for Shell cog (Linux/Shell Commands)"""

    def test_cog_initialization(self, shell_cog, bot):
        """Test that Shell cog initializes correctly"""
        assert shell_cog.bot == bot

    @pytest.mark.asyncio
    async def test_add_nobash_command(self, shell_cog):
        """Test adding user to nobash list"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        with patch('src.exts.shell.write_ignore') as mock_write:
            await shell_cog.add_nobash(inter, uid="123456")
            
            mock_write.assert_called_once_with("123456")
            inter.send.assert_called_once_with("Done")

    @pytest.mark.asyncio
    async def test_remove_nobash_command(self, shell_cog):
        """Test removing user from nobash list"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        with patch('src.exts.shell.remove_ignore') as mock_remove:
            await shell_cog.remove_nobash(inter, uid="123456")
            
            mock_remove.assert_called_once_with("123456")
            inter.send.assert_called_once_with("Done")

    @pytest.mark.asyncio
    async def test_reset_bash_without_confirmation(self, shell_cog):
        """Test reset bash without confirmation"""
        inter = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 123456

        await shell_cog.reset_bash(inter, confirm="n")

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "confirm" in call_args.lower()

    @pytest.mark.asyncio
    async def test_reset_bash_with_confirmation(self, shell_cog):
        """Test reset bash with confirmation"""
        inter = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 123456

        with patch('src.exts.shell.run_command_shell') as mock_run:
            mock_run.return_value = ""
            
            await shell_cog.reset_bash(inter, confirm="y")

            assert inter.send.call_count == 2
            mock_run.assert_called()

    @pytest.mark.asyncio
    async def test_bash_forbidden_command_dd(self, shell_cog):
        """Test bash command with forbidden command (dd)"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 123456
        inter.guild = Mock()
        inter.guild.id = 123456789

        await shell_cog.bash(inter, cmd="dd if=/dev/zero of=/dev/null")

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "Do not" in call_args

    @pytest.mark.asyncio
    async def test_bash_forkbomb_detection(self, shell_cog):
        """Test bash command with forkbomb detection"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 123456
        inter.guild = Mock()
        inter.guild.id = 123456789

        with patch('src.exts.shell.write_ignore') as mock_write:
            await shell_cog.bash(inter, cmd=":(){ :|:& };:")

            inter.send.assert_called_once()
            call_args = inter.send.call_args[0][0]
            assert "forkbomb" in call_args.lower()
            mock_write.assert_called_once()

    @pytest.mark.asyncio
    async def test_bash_user_in_ignore_list(self, shell_cog):
        """Test bash command when user is in ignore list"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 123456
        inter.guild = Mock()
        inter.guild.id = 123456789

        with patch('src.exts.shell.ignore', ['123456']):
            await shell_cog.bash(inter, cmd="ls")

            inter.send.assert_called_once()
            call_args = inter.send.call_args[0][0]
            assert "No more bash" in call_args

    @pytest.mark.asyncio
    async def test_bash_unpermitted_guild(self, shell_cog):
        """Test bash command from unpermitted guild"""
        inter = AsyncMock()
        inter.send = AsyncMock()
        inter.guild = Mock()
        inter.guild.id = 999999999  # Not in permitted_guilds

        await shell_cog.bash(inter, cmd="ls")

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "not permitted" in call_args

    @pytest.mark.asyncio
    async def test_bash_valid_command(self, shell_cog):
        """Test bash command with valid command"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.id = 123456
        inter.guild = Mock()
        inter.guild.id = 123456789

        with patch('src.exts.shell.run_command_shell') as mock_run, \
             patch('os.urandom') as mock_random:
            mock_random.return_value = b'testfile'
            mock_run.return_value = "output"
            
            # Mock that user doesn't exist
            mock_run.side_effect = [
                "n",  # has_user check
                "",   # mk_user
                "",   # scp temp script
                "",   # chmod
                "test output",  # ssh execute
                ""    # rm temp script
            ]

            await shell_cog.bash(inter, cmd="ls")

            inter.response.defer.assert_called_once()
            inter.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_mbash_command(self, shell_cog):
        """Test mbash command (owner only)"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()

        with patch('src.exts.shell.run_command_shell') as mock_run:
            mock_run.return_value = "command output"
            
            await shell_cog.mbash(inter, cmd="ls -la")

            inter.response.defer.assert_called_once()
            mock_run.assert_called_once_with("ls -la")
            inter.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_mbash_long_output(self, shell_cog):
        """Test mbash with long output"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()

        with patch('src.exts.shell.run_command_shell') as mock_run, \
             patch('src.exts.shell.paste') as mock_paste:
            mock_run.return_value = "x" * 2000
            mock_paste.return_value = "http://paste.example.com"
            
            await shell_cog.mbash(inter, cmd="ls")

            mock_paste.assert_called_once()
            inter.send.assert_called_once()


# NOTES ON MODULE ORGANIZATION:
# - Shell module is appropriately categorized for Linux/shell commands
# - Security measures in place (forbidden commands, forkbomb detection)
# - Guild permission checking is appropriate
