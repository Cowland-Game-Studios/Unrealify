from Handlers import KeyStrokeHandler
import threading

if __name__ == "__main__":
  #have background thread doing the keystroke detection with event hooked up here, and when event hits refocus window