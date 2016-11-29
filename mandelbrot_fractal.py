from PIL import Image
import argparse
import sys
import winsound          
import time             
import collections


# source: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '=' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

colors = [(0,0,0), (255,0,0), (0,255,0), (0,0,255)]

def Draw_Fractal(type, dimension, max_iteration, viewport):
    pixels = {}
    width = int(dimension[0])
    height = int(dimension[1])
    viewport_width = abs(viewport[0] - viewport[1])
    viewport_height = abs(viewport[2] - viewport[3])
    
    for h in range(height):
        printProgress(h, height, 'Mandelbrot calculation:', '', 1, 40)
        for w in range(width):
            x0 = (w / dimension[0]) * viewport_width + viewport[0]
            y0 = (h / dimension[1]) * viewport_height + viewport[2]
            x = 0.0
            y = 0.0
            iteration = 0
            while x*x + y*y < 1024 and iteration < max_iteration:
                tmp = x*x -y*y + x0
                y = 2*x*y + y0
                x = tmp
                iteration += 1
            
            pixels[(w,h)] = iteration
            
            
    histogram = collections.Counter(pixels.values())
    total = float(sum(histogram.values()))
    pixelcolors = []        
            
    for h in range(height):        
        printProgress(h, height, 'Color calculation:', '', 1, 40)
        for w in range(width):
            hue = 0.0
            for i in range(pixels[(w,h)]):
                hue += histogram[i] / total
                
            if pixels[(w,h)] >= max_iteration:
                color = 255, 255/2, 0
            else:
                color = 0, int(255.0/2 * hue), int(0.4 * 255.0 * (1 - hue))
                
            pixelcolors.append(color)
            
            
    im = Image.new('RGB', (width, height))
    im.putdata(pixelcolors)
    im.save('fractal.png')
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dimension', default='7680*4320', required=False, type=str, 
                       help='Describe the image dimensionality in the format of [width]*[height]')
    parser.add_argument('--max_iteration', default=300, required=False, type=int, 
                       help='How many iterations should the algo do?')
    parser.add_argument('--viewport', default='-2.5,1,-1.0,1.0', required=False, type=str, 
                       help='Describe the mandelbrot viewport in the format of [xmin],[xmax],[ymin],[ymax]')
    
    args = parser.parse_args()
    viewport = [float(string) for string in args.viewport.split(',')]
    dimension = [float(string) for string in args.dimension.split('*')]
    Draw_Fractal(args.type, dimension, args.max_iteration, viewport)
    winsound.Beep(600, 250)
    time.sleep(0.15) 

    