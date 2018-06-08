from __future__ import division
from PIL import ImageDraw, ImageFont


def paintNode(image, x, y, node, mandatory, nodeHighestCon):
    letter = ImageFont.truetype("Arial Bold.ttf", 12)
    drawing = ImageDraw.Draw(image)
    ellipseSize = (x, y, x+30, y+30)
    if mandatory == 1:
        if node == 'N1':
            drawing.rectangle(ellipseSize, fill=(168, 168, 170), outline=(114, 114, 115))
        elif node == nodeHighestCon:
            drawing.ellipse(ellipseSize, fill=(255, 0, 0), outline=(114, 114, 115))
        else:
            drawing.ellipse(ellipseSize, fill=(168, 168, 170), outline=(140, 141, 144))
    else:
        if node == nodeHighestCon:
            drawing.ellipse(ellipseSize, fill=(255, 0, 0), outline=(114, 114, 115))
        else:
            drawing.ellipse(ellipseSize, fill=(229, 230, 232), outline=(140, 141, 144))
    w, h = drawing.textsize(node)
    l = 0
    drawing.text((((30 - w) / 2) + x, ((30 - h) / 2) + y + l), node, fill='black', font=letter, anchor=None)
    return image

def paintArc(image, xyStart, xyEnd):
    dibujo = ImageDraw.Draw(image)
    dibujo.line((xyStart, xyEnd), fill=(245, 153, 138), width=3)
    return image

def arcName(image, arcs, mine):
    letter = ImageFont.truetype("Arial.ttf", 13)
    drawing = ImageDraw.Draw(image)
    yA = 0
    yS = 0

    if mine == "ElAlisal":
        x = 100
        yA = 850
        yS = 0
        drawing.rectangle((x - 10, yA - 30, x + 400, yA + 180), fill=(255, 255, 255), outline=(114, 114, 115))
        drawing.line(((x - 10, yA - 10), (x + 400, yA - 10)), fill=(114, 114, 115), width=2)
        drawing.text((x + 150, yA - 25), 'ARCS', fill='black', font=letter, anchor=None)


    elif mine == "Sena":
        drawing.rectangle((10, 588, 393, 780), fill=(255, 255, 255), outline=(114, 114, 115))
        drawing.line(((10, 608), (758, 608)), fill=(114, 114, 115), width=2)
        drawing.text((190, 590), 'ARCS', fill='black', font=letter, anchor=None)
        x = 20
        yS = 615
        yA = 0

    cont = 0
    y = yA + yS
    for arc in arcs:
        cont = cont + 1
        drawing.text((x,y), arc[0] + ' - ' + arc[1] + ': ' + str(arc[2]), fill='black', font=letter, anchor=None)
        y = y + 15
        if cont == 10:
            cont =0
            x = x + 140
            y = yA + yS
    return image

def WSNLegend(image, mine):
    if mine == 'ElAlisal':
        letter = ImageFont.truetype("Arial.ttf", 28)
        drawing = ImageDraw.Draw(image)
        x = 900
        y = 800
        drawing.rectangle((x, y, 560 + x, 230 + y), fill=(255, 255, 255), outline=(114, 114, 115))
        drawing.rectangle((15 + x, 15 + y, 55 + x, 55 + y), fill=(140, 141, 144), outline=(114, 114, 115))
        drawing.text((70 + x, 15 + y), 'Base Station', fill='black', font=letter, anchor=None)
        drawing.ellipse((15 + x, 70 + y, 55 + x, 110 + y), fill=(140, 141, 144), outline=(114, 114, 115))
        drawing.text((70 + x, 70 + y), 'Sensor Node', fill='black', font=letter, anchor=None)
        drawing.ellipse((15 + x, 125 + y, 55 + x, 165 + y), fill=(229, 230, 232), outline=(170, 171, 173))
        drawing.text((70 + x, 125 + y), 'Relay Node', fill='black', font=letter, anchor=None)
        drawing.ellipse((15 + x, 180 + y, 55 + x, 220 + y), fill=(255, 0, 0), outline=(170, 171, 173))
        drawing.text((70 + x, 180 + y), 'Highest energy consumption node', fill='black', font=letter, anchor=None)
    elif mine == "Sena":
        letter = ImageFont.truetype("Arial.ttf", 16)
        drawing = ImageDraw.Draw(image)
        x = 378
        y = 15
        drawing.rectangle((15 + x, 573 + y, 380 + x, 765 + y), outline=(114, 114, 115))
        drawing.text((130 + x, 574 + y), 'WSN Legend', fill='black', font=letter, anchor=None)
        drawing.rectangle((30 + x, 603 + y, 55 + x, 628 + y), fill=(140, 141, 144), outline=(114, 114, 115))
        drawing.text((68 + x, 606 + y), 'Base Station', fill='black', font=letter, anchor=None)
        drawing.ellipse((30 + x, 638 + y, 55 + x, 663 + y), fill=(140, 141, 144), outline=(114, 114, 115))
        drawing.text((68 + x, 640 + y), 'Sensor Node', fill='black', font=letter, anchor=None)
        drawing.ellipse((30 + x, 673 + y, 55 + x, 698 + y), fill=(229, 230, 232), outline=(170, 171, 173))
        drawing.text((68 + x, 673 + y), 'Relay Node', fill='black', font=letter, anchor=None)
        drawing.ellipse((30 + x, 706 + y, 55 + x, 731 + y), fill=(255, 0, 0), outline=(170, 171, 173))
        drawing.text((68 + x, 706 + y), 'Highest energy consumption node', fill='black', font=letter, anchor=None)
        drawing.rectangle((10, 10, 758, 780), outline=(114, 114, 115))
    return image
