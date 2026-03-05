import Quartz
from CoreFoundation import NSURL
import sys
import os

def pdf_to_png_target_width(pdf_path, png_path, target_width=3840):
    print(f"Loading {pdf_path}")
    url = NSURL.fileURLWithPath_(pdf_path)
    pdf = Quartz.CGPDFDocumentCreateWithURL(url)
    if not pdf: 
        print(f"Failed to load pdf {pdf_path}")
        return
    page = Quartz.CGPDFDocumentGetPage(pdf, 1)
    
    rect = Quartz.CGPDFPageGetBoxRect(page, Quartz.kCGPDFMediaBox)
    width = Quartz.CGRectGetWidth(rect)
    height = Quartz.CGRectGetHeight(rect)
    
    scale = target_width / width
    pixel_width = int(width * scale)
    pixel_height = int(height * scale)
    
    color_space = Quartz.CGColorSpaceCreateDeviceRGB()
    context = Quartz.CGBitmapContextCreate(None, pixel_width, pixel_height, 8, 4 * pixel_width, color_space, Quartz.kCGImageAlphaPremultipliedLast)
    
    if not context:
        print("Failed to create context")
        return

    Quartz.CGContextSetFillColorWithColor(context, Quartz.CGColorCreate(color_space, [1.0, 1.0, 1.0, 1.0]))
    Quartz.CGContextFillRect(context, Quartz.CGRectMake(0, 0, pixel_width, pixel_height))
    
    Quartz.CGContextSetInterpolationQuality(context, Quartz.kCGInterpolationHigh)
    Quartz.CGContextScaleCTM(context, scale, scale)
    Quartz.CGContextDrawPDFPage(context, page)
    
    image = Quartz.CGBitmapContextCreateImage(context)
    dest_url = NSURL.fileURLWithPath_(png_path)
    destination = Quartz.CGImageDestinationCreateWithURL(dest_url, 'public.png', 1, None)
    Quartz.CGImageDestinationAddImage(destination, image, None)
    Quartz.CGImageDestinationFinalize(destination)
    print(f"Saved {png_path} at {pixel_width}x{pixel_height}")

for f in os.listdir("CUSTOMER JOURNEY"):
    if f.endswith(".pdf"):
        pdf_path = os.path.join("CUSTOMER JOURNEY", f)
        png_path = os.path.join("CUSTOMER JOURNEY", f.replace(".pdf", ".png"))
        pdf_to_png_target_width(pdf_path, png_path, 3840)
