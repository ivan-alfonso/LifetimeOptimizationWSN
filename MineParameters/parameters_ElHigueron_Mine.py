
def nodes():
    # WSN nodes
    nodes = ['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9', 'N10',
             'N11', 'N12', 'N13', 'N14', 'N15', 'N16', 'N17', 'N18', 'N19',
             'N20', 'N21', 'N22', 'N23', 'N24', 'N25', 'N26', 'N27', 'N28',
             'N29', 'N30', 'N31', 'N32', 'N33', 'N34', 'N35', 'N36', 'N37']
    return nodes

def nodesM():
    # Mandatory nodes
    nodesM = ['N1', 'N11', 'N6', 'N13', 'N21', 'N30', 'N33', 'N35', 'N36', 'N37']
    return nodesM

def nodeBS():
    # Base Station node
    nodeBS = 'N1'
    return nodeBS

def arcsDistance():
    distance = {
        ('N1', 'N2'): 43.1, ('N1', 'N7'): 79.2, ('N1', 'N14'): 108.9, ('N1', 'N24'): 120.9, ('N1', 'N37'): 47.5,
        ('N2', 'N3'): 15.5, ('N2', 'N4'): 51.4, ('N2', 'N7'): 36.1, ('N2', 'N14'): 65.8, ('N2', 'N24'): 77.8,
        ('N3', 'N4'): 36, ('N3', 'N5'): 54.4, ('N3', 'N8'): 27.4, ('N3', 'N16'): 55.2,
        ('N4', 'N5'): 19.1, ('N4', 'N9'): 32.5, ('N4', 'N18'): 60.2, ('N4', 'N6'): 47.7,
        ('N5', 'N6'): 29.1,
        ('N7', 'N8'): 27.8, ('N7', 'N9'): 63.9, ('N7', 'N10'): 85.9, ('N7', 'N13'): 122.6, ('N7', 'N14'): 27,
        ('N7', 'N24'): 39, ('N7', 'N22'): 50.9, ('N7', 'N12'): 98.1,
        ('N8', 'N16'): 28, ('N8', 'N9'): 34, ('N8', 'N10'): 52.3, ('N8', 'N12'): 67.6, ('N8', 'N13'): 92.7,
        ('N9', 'N18'): 27.4, ('N9', 'N10'): 22, ('N9', 'N12'): 33.8, ('N9', 'N13'): 58.9,
        ('N10', 'N19'): 27.9, ('N10', 'N29'): 47.5, ('N10', 'N11'): 11.7, ('N10', 'N12'): 13.6, ('N10', 'N13'): 38.7,
        ('N12', 'N20'): 30.2, ('N12', 'N13'): 25.1,
        ('N14', 'N15'): 32.3, ('N14', 'N16'): 37.5, ('N14', 'N17'): 59.4, ('N14', 'N18'): 65.9, ('N14', 'N19'): 86.4,
        ('N14', 'N20'): 99.2, ('N14', 'N21'): 110.2,
        ('N15', 'N16'): 5.2, ('N15', 'N17'): 27, ('N15', 'N18'): 33.7, ('N15', 'N19'): 54.1, ('N15', 'N20'): 67,
        ('N15', 'N21'): 77.9, ('N15', 'N27'): 23.5,
        ('N16', 'N17'): 21.9, ('N16', 'N18'): 28.4, ('N16', 'N19'): 48.9, ('N16', 'N20'): 61.7, ('N16', 'N21'): 72.7,
        ('N17', 'N18'): 6.6, ('N17', 'N19'): 27, ('N17', 'N20'): 39.8, ('N17', 'N21'): 51, ('N17', 'N28'): 20.6,
        ('N18', 'N19'): 20.5, ('N18', 'N20'): 33.5, ('N18', 'N21'): 44.3,
        ('N19', 'N20'): 12.8, ('N19', 'N21'): 23.7, ('N19', 'N29'): 19.2,
        ('N22', 'N23'): 44.7, ('N22', 'N31'): 83.3, ('N22', 'N36'): 104.5, ('N22', 'N37'): 137.4,
        ('N23', 'N24'): 56.3, ('N23', 'N31'): 38.7, ('N23', 'N36'): 59.9, ('N23', 'N37'): 182.3,
        ('N24', 'N25'): 14.7, ('N24', 'N32'): 30, ('N24', 'N33'): 36.6,
        ('N25', 'N26'): 28.7, ('N25', 'N27'): 35.1, ('N25', 'N28'): 66.1, ('N25', 'N29'): 94.6, ('N25', 'N30'): 114.7,
        ('N25', 'N32'): 15.4, ('N25', 'N33'): 22,
        ('N26', 'N27'): 6.4, ('N26', 'N28'): 37.3, ('N26', 'N29'): 66, ('N26', 'N30'): 86, ('N26', 'N34'): 13.8,
        ('N27', 'N28'): 30.9, ('N27', 'N29'): 59.6, ('N27', 'N30'): 79.6,
        ('N28', 'N29'): 28.5, ('N28', 'N30'): 48.6,
        ('N29', 'N30'): 20.1,
        ('N31', 'N32'): 63.3, ('N31', 'N34'): 97.5, ('N31', 'N35'): 103.2, ('N31', 'N36'): 20.7,
        ('N32', 'N33'): 6.6, ('N32', 'N34'): 34.2, ('N32', 'N35'): 39.9,
        ('N34', 'N35'): 5.7}
    return distance