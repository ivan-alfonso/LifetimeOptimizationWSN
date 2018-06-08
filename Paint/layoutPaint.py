from MineParameters import parameters_Sena_Mine, parameters_ElAlisal_Mine
from PIL import Image

import paint
from MineParameters import parameters_ElAlisal_Mine


def paintResults(nodes, arcs, mine, mandatoryNodes, nodeHighestCons):
    if mine == "Sena":
        nodesPosicion = parameters_Sena_Mine.imageNodes()
        ImName = "Paint/MinaSena.png"
    if mine == "ElAlisal":
        nodesPosicion = parameters_ElAlisal_Mine.imageNodes()
        ImName = "Paint/MinaElAlisal.png"

    image = Image.open(ImName)

    # Paint arcs
    for arc in arcs:
        xyStart = (nodesPosicion[arc[0]][0] + 15, nodesPosicion[arc[0]][1] + 15)
        xyEnd = (nodesPosicion[arc[1]][0] + 15, nodesPosicion[arc[1]][1] + 15)
        image = paint.paintArc(image, xyStart, xyEnd)

    paint.arcName(image, arcs, mine)

    # Paint nodes
    for paintNode in nodes:
        x, y = nodesPosicion[paintNode]
        if paintNode in mandatoryNodes:
            mandatory = 1
        else:
            mandatory = 0
        image = paint.paintNode(image, x, y, paintNode, mandatory, nodeHighestCons)

    # WSN Legend
    paint.WSNLegend(image, mine)

    # Show image
    image.show()

