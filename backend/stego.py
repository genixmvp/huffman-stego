from PIL import Image
import io

def encode_message(image_bytes, bit_string):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    pixels = img.load()
    width, height = img.size
    
    # Añadimos un delimitador para saber dónde termina el mensaje (ej: 16 ceros)
    data = bit_string + '0000000000000000' 
    data_idx = 0
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # Modificamos el Bit Menos Significativo (LSB) de cada canal
            channels = [r, g, b]
            for i in range(3):
                if data_idx < len(data):
                    # Reemplazamos el último bit con el bit de nuestro mensaje
                    channels[i] = (channels[i] & ~1) | int(data[data_idx])
                    data_idx += 1
            
            pixels[x, y] = tuple(channels)
            if data_idx >= len(data):
                break
        if data_idx >= len(data):
            break
            
    output = io.BytesIO()
    img.save(output, format="PNG") # PNG es obligatorio para no perder datos
    return output.getvalue()