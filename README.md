# GamerbotAgain
Gamerbot with slash commands

## Requirements
* Docker
 
## How to run
* copy `bot/config.example.toml` to `bot/config.toml` and edit as needed
* `sudo make base`
* `sudo make replace`

## Note:
`make replace` doesn't rebuild the "base" image `gamerthebase`, to save on dev time.