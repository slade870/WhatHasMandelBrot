from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))
    for i in range(width):
        for j in range(height):
            n3[i, j] = mandelbrot(r1[i] + 1j*r2[j], max_iter)
    return (r1, r2, n3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    xmin = float(data['xmin'])
    xmax = float(data['xmax'])
    ymin = float(data['ymin'])
    ymax = float(data['ymax'])
    width = int(data['width'])
    height = int(data['height'])
    max_iter = int(data['max_iter'])
    
    x, y, mandelbrot_image = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)
    
    plt.figure(figsize=(10, 10))
    plt.imshow(mandelbrot_image.T, extent=[xmin, xmax, ymin, ymax], cmap='twilight_shifted', interpolation='bilinear')
    plt.colorbar(label='Iteration count')
    plt.title('Mandelbrot Set')
    plt.xlabel('Re')
    plt.ylabel('Im')
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    
    return jsonify({'image': plot_url})

if __name__ == '__main__':
    app.run(debug=True)
