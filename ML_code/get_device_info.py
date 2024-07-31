#%%
import pyaudio

# Initialize PyAudio
p = pyaudio.PyAudio()

# Loop over the range of device indices
for i in range(p.get_device_count()):
    # Get device information
    device_info = p.get_device_info_by_index(i)
    # Print the index and name of the device
    print(f"Index: {i}, Name: {device_info['name']}, Channels: {device_info['maxInputChannels']}")

# Terminate the PyAudio instance
p.terminate()

# %%
