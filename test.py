from concurrent.futures import process
import marker

def colored(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[38;2;255;255;255m"

text = 'It was supposed to be a dream vacation. They had planned it over a year in advance so that it would be perfect in every way. It had been what they had been looking forward to through all the turmoil and negativity around them. It had been the light at the end of both their tunnels. Now that the dream vacation was only a week away, the virus had stopped all air travel.'
boldness = marker.text_processing.process(text)
for i in range(len(text)):
    boldness[i] = int(boldness[i] * 255)
    print(colored(boldness[i], boldness[i], boldness[i], text[i]), end='')
print()