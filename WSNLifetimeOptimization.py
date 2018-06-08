from gurobipy import *
from MineParameters import parameters_Sena_Mine, parameters_ElAlisal_Mine, parameters_ElHigueron_Mine
from Paint import layoutPaint

for ite in [0,1]:
    try:
        # Parameters
        lf = 1              # Lifetime in days
        coverage = 0        # Number of nodes per section
        fr = 6              # Monitoring frequency per minute
        windowsTime = 2     # Number of windows time

        # Parameters of energy consumption
        Eelec = 50e-9     # Energy consumed by the circuit in sending and receiving by bit (nJ/bit)
        Emp = 0.0013e-12  # Energy dissipated by the multipath model transmission amplifier (pJ/bit/m4)
        Efs = 10e-12      # Energy dissipated by the freespace model transmission amplifier (pJ/bit/m2)
        cProc = 1e-4      # Consumption energy of data processing
        cSens = 1e-4      # Sensing consumption energy
        B = 4000          # Battery capacity
        bits = 4000       # Data packet size
        do = 87           # threshold distance (m)
        samples = fr * 60 * 8 * lf  # number of samples for the lifetime

        # Parametros de agrupacion de nodos SENA
        grupoN1 = ['N1', 'N2', 'N11', 'N12']
        grupoN2 = ['N3', 'N4', 'N5', 'N6']
        grupoN3 = ['N13', 'N14', 'N15', 'N16', 'N17', 'N18']
        grupoN4 = ['N7', 'N8', 'N9', 'N10']
        grupoN5 = ['N19', 'N20', 'N21', 'N22']
        mandatoryNode1 = []
        mandatoryNode2 = []
        mandatoryNode3 = []
        mandatoryNode4 = []

        # Mine
        mine = "Sena"
        #mine = "ElAlisal"
        #mine = "ElHigueron"

        # WSN Nodes for each mine
        if mine == "Sena":
            nodes = parameters_Sena_Mine.nodes()
            nodesM = parameters_Sena_Mine.nodesM()
            nodeBS = parameters_Sena_Mine.nodeBS()
            distance = parameters_Sena_Mine.arcsDistance()
            arcs = distance.keys()
        elif mine == "ElAlisal":
            nodes = parameters_ElAlisal_Mine.nodes()
            nodesM = parameters_ElAlisal_Mine.nodesM()
            nodeBS = parameters_ElAlisal_Mine.nodeBS()
            distance = parameters_ElAlisal_Mine.arcsDistance()
            arcs = distance.keys()
        elif mine == "ElHigueron":
            nodes = parameters_ElHigueron_Mine.nodes()
            nodesM = parameters_ElHigueron_Mine.nodesM()
            nodeBS = parameters_ElHigueron_Mine.nodeBS()
            distance = parameters_ElHigueron_Mine.arcsDistance()
            arcs = distance.keys()

        for arc in range(len(arcs)):
            arcs.append((arcs[arc][1], arcs[arc][0]))
            distance[arcs[arc][1], arcs[arc][0]] = distance[arcs[arc][0], arcs[arc][1]]

        costSensor = 10000
        capacity = 30

        #Power consumption of transmission of a data packet for each node
        Tx = {}
        for arc in arcs:
            if distance[arc] >= do:
                Tx[arc] = Eelec + (Emp * (distance[arc] ** 4))
            if distance[arc] < do:
                Tx[arc] = Eelec + (Efs * (distance[arc] ** 2))

        nodesOn = []
        arcsOn1 = []
        arcsOn2 = []
        arcsOn3 = []
        arcsOn4 = []
        maxConsumption = 0

        tNodes = []
        tArcs = []
        times = []
        for t in range(windowsTime):
            times.append(t + 1)
        for i in times:
            for j in nodes:
                tNodes.append((j, i))
            for h in arcs:
                tArcs.append((h[0], h[1], i))


        #---CREACION DEL MODELO---
        m = Model("mip1")

        #---DECISION VARIABLES---
        x = m.addVars(nodes, vtype=GRB.BINARY, name="x")
        y = m.addVars(arcs, vtype=GRB.BINARY, name="y")
        w = m.addVars(tArcs, vtype=GRB.INTEGER, name="w")
        z = m.addVar(vtype=GRB.INTEGER, name="z")
        aa = m.addVars(tNodes, vtype=GRB.BINARY, name="aa")
        m.update()

        #---OBJECTIVE FUNCTION---

        # Calculation of costs
        costos = sum(x[i] * costSensor for i in nodes)

        # Objective function
        m.setObjective((costos * (1 - ite)) + (z * ite), GRB.MINIMIZE)

        #---CONSTRAINTS----

        # Mandatory sensors constraint
        m.addConstrs((x[i] == 1 for i in nodesM), "SensorO")

        # Conectivity constraint
        m.addConstrs((y[i] >= x[i[0]] + x[i[1]] - 1 for i in arcs), "LineaVistaA")
        m.addConstrs((y[i] <= (x[i[0]] + x[i[1]]) / 2 for i in arcs), "LineaVistaB")

        # Flow conservation constraint
        m.addConstrs((w[i] >= 0 for i in tArcs), "FlujoArcoA")
        m.addConstrs((w[i] <= y[(i[0],i[1])] * capacity for i in tArcs), "FlujoArcoB")

        for t in times:
            for i in nodes:
                sale = quicksum(w[i, j, t] for j in nodes if (i, j) in arcs)
                entra = quicksum(w[j, i, t] for j in nodes if (j, i) in arcs)
                if i == nodeBS:
                    m.addConstr(sale - entra == - (quicksum(aa[nodo, t] for nodo in nodes) - 1), "Demanda_BS" + str(i))
                else:
                    m.addConstr(sale - entra == aa[i, t], "Demanda_" + str(i))

        # Restricciones para modos de operacion
        m.addConstrs((aa[i, t] == 1 for i in nodesM for t in times), "Modo")
        m.addConstrs((x[i] >= aa[i, t] for i in nodesM for t in times), "Modo")

        # Lifetime constraints
        for i in nodes:
            if i <> nodeBS:
                Etx = quicksum((w[i, j, t] * Tx[i, j] * bits) for j in nodes if (i, j) in arcs for t in times)
                Erx = quicksum((w[j, i, t] * Eelec * bits) for j in nodes if (j, i) in arcs for t in times)
                EProc = quicksum(aa[i, t] * cProc for t in times)
                ESens = quicksum(aa[i, t] * cSens for t in times)
                if ite == 0:
                    m.addConstr(((Etx + Erx + EProc + ESens) * (samples / windowsTime) <= B), "Energia_" + str(i))
                if ite == 1:
                    m.addConstr(((Etx + Erx + EProc + ESens) * 10000000 <= z), "Energia_" + str(i))

        # Maximun nodes constraint
        if ite == 1:
            m.addConstr((quicksum(x[i] for i in nodes) == numNodes), "CantSensores")

        # Coverage constraints
        # for t in tiempos:
        #     m.addConstr(quicksum(aa[i, t] for i in grupoN1) >= coverage, "coverageG1")
        #     m.addConstr(quicksum(aa[i, t] for i in grupoN2) >= coverage, "coverageG2")
        #     m.addConstr(quicksum(aa[i, t] for i in grupoN3) >= coverage, "coverageG3")
        #     m.addConstr(quicksum(aa[i, t] for i in grupoN4) >= coverage, "coverageG4")

        #---OPTIMIZE MODEL---
        m.optimize()

        #---RESULTS-----
        # Print content of variables that are greater than zero
        for v in m.getVars():
            if v.x > 1e-3:
                print('%s %g' % (v.varName, v.x))

        # Print value of the objective function
        print('Obj: %g' % m.objVal)

        # Store active nodes (x) and active communications (y)
        for var in m.getVars():
            if var.varName.find('x') <> -1 and var.x > .9:
                nodesOn.append(var.varName[var.varName.find('[') + 1:var.varName.find(']')])
            if var.varName.find('w') <> -1 and var.x > .9:
                coma = ([pos for pos, char in enumerate(var.varName) if char == ','])
                if var.varName[coma[1] + 1:var.varName.find(']')] == '1':
                    arcsOn1.append((var.varName[var.varName.find('[') + 1:coma[0]],
                                    var.varName[coma[0] + 1:coma[1]],
                                    var.x))
                if var.varName[coma[1] + 1:var.varName.find(']')] == '2':
                    arcsOn2.append((var.varName[var.varName.find('[') + 1:coma[0]],
                                    var.varName[coma[0] + 1:coma[1]],
                                    var.x))
                if var.varName[coma[1] + 1:var.varName.find(']')] == '3':
                    arcsOn3.append((var.varName[var.varName.find('[') + 1:coma[0]],
                                    var.varName[coma[0] + 1:coma[1]],
                                    var.x))
                if var.varName[coma[1] + 1:var.varName.find(']')] == '4':
                    arcsOn4.append((var.varName[var.varName.find('[') + 1:coma[0]],
                                    var.varName[coma[0] + 1:coma[1]],
                                    var.x))

        # Store the nodes that are sensors for each time window
        for var in m.getVars():
            if var.varName.find('aa') <> -1 and var.x > .9:
                if var.varName[var.varName.find(',')+1:var.varName.find(']')] == "1":
                    mandatoryNode1.append(var.varName[var.varName.find('[')+1:var.varName.find(',')])
                if var.varName[var.varName.find(',')+1:var.varName.find(']')] == "2":
                    mandatoryNode2.append(var.varName[var.varName.find('[')+1:var.varName.find(',')])
                if var.varName[var.varName.find(',')+1:var.varName.find(']')] == "3":
                    mandatoryNode3.append(var.varName[var.varName.find('[')+1:var.varName.find(',')])
                if var.varName[var.varName.find(',')+1:var.varName.find(']')] == "4":
                    mandatoryNode4.append(var.varName[var.varName.find('[')+1:var.varName.find(',')])


        if ite == 1:
            for var in m.getVars():
                if var.varName.find('z') <> -1:
                    maxConsumption = var.x / 10000000

        # Get the nodes that consume the most energy in each time window
        if ite == 1:
            nodoCritico = []
            for t in times:
                consumption = {}
                for i in nodes:
                    if i <> nodeBS:
                        Etx = quicksum((m.getVarByName('w[' + i + ',' + j + ',' + str(t) + ']').x * Tx[i, j] * bits)
                                       for j in nodes if (i, j) in arcs)
                        Erx = quicksum((m.getVarByName('w[' + j + ',' + i + ',' + str(t) + ']').x * Eelec * bits)
                                       for j in nodes if (j, i) in arcs)
                        EProc = m.getVarByName('aa[' + i + ',' + str(t) + ']').x * cProc
                        ESens = m.getVarByName('aa[' + i + ',' + str(t) + ']').x * cSens
                        consumption[i] = Etx.getValue() + Erx.getValue() + EProc + ESens
                nodoCritico.append(max(consumption, key=consumption.get))
                print "Time window" , t, " - Node with the highest consumption: ", max(consumption, key=consumption.get), " - consumption: ", consumption.get(max(consumption, key=consumption.get))

        # Get the node that consumes the most energy in the entire WSN
        consumption = {}
        for i in nodes:
            if i <> nodeBS:
                Erx = quicksum((m.getVarByName('w[' + j + ',' + i + ',' + str(t) + ']').x * Eelec * bits)
                               for j in nodes if (j, i) in arcs for t in times)
                Etx = quicksum((m.getVarByName('w[' + i + ',' + j + ',' + str(t) + ']').x * Tx[i, j] * bits)
                               for j in nodes if (i, j) in arcs for t in times)
                EProc = quicksum(m.getVarByName('aa[' + i + ',' + str(t) + ']').x * cProc for t in times)
                ESens = quicksum(m.getVarByName('aa[' + i + ',' + str(t) + ']').x * cSens for t in times)
                consumption[i] = Etx.getValue() + Erx.getValue() + EProc.getValue() + ESens.getValue()
        print "Node with the highest energy consumption: ", max(consumption, key=consumption.get), " - consumption: ", consumption.get(max(consumption, key=consumption.get))


    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')

    numNodes = len(nodesOn)

    # Print WSN in the layout of the mine
    if ite == 1 and mine <> "ElHigueron":
        if windowsTime >= 1:
            layoutPaint.paintResults(nodesOn, arcsOn1, mine, mandatoryNode1, nodoCritico[0])
        elif windowsTime >= 2:
            layoutPaint.paintResults(nodesOn, arcsOn2, mine, mandatoryNode2, nodoCritico[1])
        elif windowsTime >= 3:
            layoutPaint.paintResults(nodesOn, arcsOn3, mine, mandatoryNode3, nodoCritico[2])
        elif windowsTime >= 4:
            layoutPaint.paintResults(nodesOn, arcsOn4, mine, mandatoryNode4, nodoCritico[3])

lifetime = B / (maxConsumption * fr * 60 * (8.0 / windowsTime))
print "With ", numNodes, " nodes - maximum lifetime ", lifetime, "days"