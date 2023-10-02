import subprocess

def sniff_text_messages(interface):
  """Sniffs text messages on the given interface.

  Args:
    interface: The name of the interface to sniff on.

  Returns:
    A list of text message strings.
  """

  # Use the tcpdump command with root privileges to sniff all TCP traffic on the given interface.
  tcpdump_output = subprocess.check_output(["sudo", "tcpdump", "-i", interface, "tcp and port 80"])

  # Extract the text messages from the tcpdump output.
  text_messages = []
  for line in tcpdump_output.decode().split("\n"):
    if "text=" in line:
      text_message = re.findall(r"text=([^&]+)", line)
      if text_message:
        text_messages.append(text_message[0])

  return text_messages

def main():
  """The main function."""

  interface = "wlan0"

  text_messages = sniff_text_messages(interface)

  # Print the text messages.
  for text_message in text_messages:
    print(text_message)

if __name__ == "__main__":
  main()
