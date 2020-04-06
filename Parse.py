import chess.pgn, re

PGNS   = [
    "S13DivP.pgn",
    "S14DivP.pgn",
    "S15DivP.pgn",
    "S16DivP.pgn",
]

class Visitor(chess.pgn.BaseVisitor):

    def begin_game(self):
        self.nodes = []

    def visit_comment(self, comment):
        match = re.search('(?<= n=)[0-9]*', comment)
        self.nodes.append(int(match.group()) if match else None)

def collectNodesFromPGN(pgn):

    nodes = []

    while True:

        # Parse until out of games
        game = chess.pgn.read_game(pgn)
        if game == None: break

        # Find Houdini 6.03's colour and their games
        isWhite = game.headers["White"] == "Houdini 6.03"
        isBlack = game.headers["Black"] == "Houdini 6.03"
        if not isWhite and not isBlack: continue

        # BUG: There is one game where Fire fails to report any
        # comment. This is in S14 DivP. Found on line #26589.
        # This breaks our method of tracking node counters
        if game.headers["White"] == "Fire 7.1"      and \
           game.headers["Black"] == "Houdini 6.03"  and \
           game.headers["Round"] == "41.4":
           continue

        # Collect node counters for each player
        visitor = Visitor(); game.accept(visitor)
        whiteNodes = visitor.nodes[1::2]
        blackNodes = visitor.nodes[2::2]

        # Collect nodes for Houdini 6.03
        if isWhite: nodes.extend(whiteNodes)
        if isBlack: nodes.extend(blackNodes)

    return nodes

def parsePGN(fname):
    with open(fname, "r") as pgn:
        return collectNodesFromPGN(pgn)

def parsePGNs():

    # Find node count for Houdini 6.03 in all PGNS
    games = [parsePGN(fname) for fname in PGNS]
    nodes = [node for game in games for node in game if node != None]
    for node in nodes: print(node)

    # Generator Histogram [0, 7)
    histo = {f:0 for f in range(8)}
    for node in nodes: histo[node%8] = histo[node%8] + 1
    print (histo)

    for node in nodes:
        if node % 8 == 7:
            print node

parsePGNs()
