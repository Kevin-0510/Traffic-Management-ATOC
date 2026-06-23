import sumolib

net = sumolib.net.readNet(
    r"E:\Downloads\Agentic Traffic management\sumo\network\cross_intersection.net.xml"
)

for edge in net.getEdges():
    print("\nEDGE:", edge.getID())

    frm = edge.getFromNode().getID()
    to = edge.getToNode().getID()

    print("FROM:", frm)
    print("TO:", to)

    print("FROM COORD:", edge.getFromNode().getCoord())
    print("TO COORD:", edge.getToNode().getCoord())