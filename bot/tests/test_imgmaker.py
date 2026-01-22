"""Tests for imgmaker module (Image Manipulation)"""
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import disnake
from disnake.ext import commands


@pytest.fixture
def bot():
    """Create a mock bot instance"""
    return Mock(spec=commands.Bot)


@pytest.fixture
def imgmaker_cog(bot):
    """Create ImageMaker cog instance"""
    with patch('toml.load'):
        from src.exts.imgmaker import ImageMaker
        return ImageMaker(bot)


class TestImageMaker:
    """Test suite for ImageMaker cog (Image Manipulation)"""

    def test_cog_initialization(self, imgmaker_cog, bot):
        """Test that ImageMaker cog initializes correctly"""
        assert imgmaker_cog.bot == bot

    def test_calculate_font_size_short_text(self, imgmaker_cog):
        """Test font size calculation for short text"""
        size = imgmaker_cog._calculate_font_size("short")
        assert size == 50  # base_size for text <= 10 chars

    def test_calculate_font_size_long_text(self, imgmaker_cog):
        """Test font size calculation for long text"""
        long_text = "a" * 30  # 30 characters
        size = imgmaker_cog._calculate_font_size(long_text)
        # For 30 chars: reduction = (30 - 10) * 0.6 = 12
        expected = 50 - 12
        assert size == expected

    def test_calculate_font_size_minimum(self, imgmaker_cog):
        """Test that font size respects minimum"""
        very_long_text = "a" * 100
        size = imgmaker_cog._calculate_font_size(very_long_text)
        assert size >= 16  # min_size

    @pytest.mark.asyncio
    async def test_figlet_success(self, imgmaker_cog):
        """Test figlet command with valid input"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()

        with patch('pyfiglet.Figlet') as mock_figlet:
            mock_figlet_instance = Mock()
            mock_figlet_instance.renderText = Mock(return_value="ASCII ART")
            mock_figlet.return_value = mock_figlet_instance

            await imgmaker_cog.figlet.callback(imgmaker_cog, inter, text="test")

            inter.response.defer.assert_called_once()
            inter.send.assert_called_once()
            call_args = inter.send.call_args[0][0]
            assert "ASCII ART" in call_args

    @pytest.mark.asyncio
    async def test_figlet_error(self, imgmaker_cog):
        """Test figlet command error handling"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()

        with patch('pyfiglet.Figlet') as mock_figlet:
            mock_figlet.side_effect = Exception("Figlet error")

            await imgmaker_cog.figlet.callback(imgmaker_cog, inter, text="test")

            inter.send.assert_called_once()
            # Check that error embed was sent
            call_args = inter.send.call_args
            assert call_args is not None

    @pytest.mark.asyncio
    async def test_onceagain_command(self, imgmaker_cog):
        """Test onceagain command (Bernie meme generator)"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.mention = "@testuser"

        with patch('PIL.Image.open') as mock_open, \
             patch('PIL.ImageDraw.Draw') as mock_draw, \
             patch('PIL.ImageFont.truetype') as mock_font, \
             patch('os.remove') as mock_remove:
            
            mock_img = Mock()
            mock_img.save = Mock()
            mock_open.return_value = mock_img

            await imgmaker_cog.onceagain.callback(imgmaker_cog, inter, text="test support")

            inter.response.defer.assert_called_once()
            mock_img.save.assert_called_with("bernie-gen.png")
            inter.send.assert_called_once()
            mock_remove.assert_called_once_with("bernie-gen.png")

    @pytest.mark.asyncio
    async def test_bugs_command(self, imgmaker_cog):
        """Test bugs command (Bugs Bunny meme generator)"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()

        with patch('PIL.Image.open') as mock_open, \
             patch('PIL.ImageDraw.Draw') as mock_draw, \
             patch('PIL.ImageFont.truetype') as mock_font, \
             patch('os.remove') as mock_remove:
            
            mock_img = Mock()
            mock_img.save = Mock()
            mock_open.return_value = mock_img

            await imgmaker_cog.bugs.callback(imgmaker_cog, inter, text_one="text1", text_two="text2")

            inter.response.defer.assert_called_once()
            mock_img.save.assert_called_with("bugs-gen.png")
            inter.send.assert_called_once()
            mock_remove.assert_called_once_with("bugs-gen.png")

    @pytest.mark.asyncio
    async def test_bonk_default(self, imgmaker_cog):
        """Test bonk command with default text"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.author.mention = "@testuser"

        with patch('PIL.Image.open') as mock_open, \
             patch('PIL.ImageDraw.Draw') as mock_draw, \
             patch('PIL.ImageFont.truetype') as mock_font, \
             patch('os.remove') as mock_remove:
            
            mock_img = Mock()
            mock_img.save = Mock()
            mock_open.return_value = mock_img

            await imgmaker_cog.bonk.callback(imgmaker_cog, inter, text="")

            inter.response.defer.assert_called_once()
            # With empty text, it should use author mention and send the static image
            inter.send.assert_called()

    @pytest.mark.asyncio
    async def test_bonk_with_user_mention(self, imgmaker_cog):
        """Test bonk command with user mention"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()
        inter.bot.fetch_user = AsyncMock()
        
        mock_user = Mock()
        mock_user.display_name = "TestUser"
        mock_user.mention = "@testuser"
        inter.bot.fetch_user.return_value = mock_user

        with patch('PIL.Image.open') as mock_open, \
             patch('PIL.ImageDraw.Draw') as mock_draw, \
             patch('PIL.ImageFont.truetype') as mock_font, \
             patch('os.remove') as mock_remove:
            
            mock_img = Mock()
            mock_img.save = Mock()
            mock_open.return_value = mock_img

            await imgmaker_cog.bonk.callback(imgmaker_cog, inter, text="<@!123456>")

            inter.bot.fetch_user.assert_called_once()
            inter.send.assert_called()

    @pytest.mark.asyncio
    async def test_pfp_command(self, imgmaker_cog):
        """Test pfp command to get user avatar"""
        inter = AsyncMock()
        inter.send = AsyncMock()
        inter.author.mention = "@caller"
        inter.bot.fetch_user = AsyncMock()
        
        mock_user = Mock()
        mock_user.display_avatar.url = "https://example.com/avatar.png"
        inter.bot.fetch_user.return_value = mock_user

        await imgmaker_cog.pfp.callback(imgmaker_cog, inter, who="<@!123456>")

        inter.bot.fetch_user.assert_called_once_with(123456)
        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "https://example.com/avatar.png" in call_args

    @pytest.mark.asyncio
    async def test_pfp_invalid_user(self, imgmaker_cog):
        """Test pfp command with invalid user mention"""
        inter = AsyncMock()
        inter.send = AsyncMock()
        inter.author.mention = "@caller"

        await imgmaker_cog.pfp.callback(imgmaker_cog, inter, who="not_a_mention")

        inter.send.assert_called_once()
        call_args = inter.send.call_args[0][0]
        assert "ain't a user" in call_args

    @pytest.mark.asyncio
    async def test_forkbomb_no_text(self, imgmaker_cog):
        """Test forkbomb command without text"""
        inter = AsyncMock()
        inter.send = AsyncMock()

        with patch('disnake.File') as mock_file:
            await imgmaker_cog.forkbomb.callback(imgmaker_cog, inter, text="")

            inter.send.assert_called_once()
            mock_file.assert_called_with("images/forkbomb.jpg")

    @pytest.mark.asyncio
    async def test_forkbomb_with_text(self, imgmaker_cog):
        """Test forkbomb command with custom text"""
        inter = AsyncMock()
        inter.response.defer = AsyncMock()
        inter.send = AsyncMock()

        with patch('PIL.Image.open') as mock_open, \
             patch('PIL.ImageDraw.Draw') as mock_draw, \
             patch('PIL.ImageFont.truetype') as mock_font, \
             patch('os.remove') as mock_remove:
            
            mock_img = Mock()
            mock_img.save = Mock()
            mock_open.return_value = mock_img

            await imgmaker_cog.forkbomb.callback(imgmaker_cog, inter, text="custom text")

            inter.response.defer.assert_called_once()
            mock_img.save.assert_called_with("fb-s.jpg")
            inter.send.assert_called_once()
            mock_remove.assert_called_once_with("fb-s.jpg")


# Note: The space command uses os.system("wget") which is a potential security issue
# and should ideally use requests or aiohttp instead
