from neomodel import StructuredNode, StringProperty, RelationshipTo

# Create your models here.


class Node(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    connections = RelationshipTo('Node','CONNECTION')

    def get_shortest_path(self, to):
        # start & end are same
        if self.name == to:
            return None

        q = "MATCH (start:Node {name: '%s'}), (end:Node {name: '%s'}), p = shortestPath((start)-[*]-(end)) RETURN p" % (self.name, to)
        results, _ = self.cypher(q)
        return results[0][0] if len(results) > 0 else None