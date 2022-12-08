import os

class VoiceState:
    def __init__(self):
        if os.path.exists(".voice_state"):
            os.remove(".voice_state")
        with open(".voice_state", "w") as f:
            f.write("0")
        return

    def check_state(self):
        with open(".voice_state") as f:
            state = f.read()
        if state == "0":  # failsafe
            return False
        else:
            return True

    def set_state(self, new):
        os.remove(".voice_state")
        with open(".voice_state", "w") as f:
            f.write(new)
