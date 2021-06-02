from django.test import TestCase
from django.test import Client

from neomodel.util import clear_neo4j_database
from neomodel import db

from .models import Node

class NodeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        clear_neo4j_database(db)

    def test_create(self):
        """
        Test Node creations
        """
        # Test other http methods
        assert len(Node.nodes.all()) == 0
        assert len(Node.nodes.filter(name='a')) == 0

        response = self.client.get('/node/create/a')
        assert response.status_code == 405

        response = self.client.put('/node/create/a')
        assert response.status_code == 405

        response = self.client.head('/node/create/a')
        assert response.status_code == 405

        response = self.client.delete('/node/create/a')
        assert response.status_code == 405

        assert len(Node.nodes.all()) == 0
        assert len(Node.nodes.filter(name='a')) == 0

        # Test API end point
        response = self.client.post('/node/create/a')
        assert response.status_code == 201
        response = response.json()
        assert 'name' in response and response['name'] == 'a'

        response = self.client.post('/node/create/b')
        assert response.status_code == 201
        response = response.json()
        assert 'name' in response and response['name'] == 'b'

        response = self.client.post('/node/create/c')
        assert response.status_code == 201
        response = response.json()
        assert 'name' in response and response['name'] == 'c'

        response = self.client.post('/node/create/d')
        assert response.status_code == 201
        response = response.json()
        assert 'name' in response and response['name'] == 'd'

        ## Verify on actual DB
        assert len(Node.nodes.all()) == 4
        assert Node.nodes.get(name='a').name == 'a'
        assert Node.nodes.get(name='b').name == 'b'
        assert Node.nodes.get(name='c').name == 'c'
        assert Node.nodes.get(name='d').name == 'd'

         ## Test duplication
        response = self.client.post('/node/create/d')
        assert response.status_code == 409
        assert len(Node.nodes.all()) == 4
        assert len(Node.nodes.filter(name='d')) == 1

    def test_connect(self):
        """
        Test Node connections
        """
        
        a = Node(name='a').save()
        b = Node(name='b').save()
        c = Node(name='c').save()
        d = Node(name='d').save()
        e = Node(name='e').save()
        f = Node(name='f').save()

        assert (len(a.connections) == 0)
        assert (len(b.connections) == 0)
        assert (len(c.connections) == 0)
        assert (len(d.connections) == 0)
        assert (len(e.connections) == 0)
        assert (len(f.connections) == 0)
        
        # Test other http methods
        assert len(Node.nodes.all()) == 6
        assert len(Node.nodes.filter(name='a')) == 1
        assert len(Node.nodes.filter(name='b')) == 1
        assert len(Node.nodes.filter(name='c')) == 1
        assert len(Node.nodes.filter(name='d')) == 1
        assert len(Node.nodes.filter(name='e')) == 1
        assert len(Node.nodes.filter(name='f')) == 1

        response = self.client.get('/node/connect/a/b')
        assert response.status_code == 405

        response = self.client.put('/node/connect/a/b')
        assert response.status_code == 405

        response = self.client.head('/node/connect/a/b')
        assert response.status_code == 405

        response = self.client.delete('/node/connect/a/b')
        assert response.status_code == 405

        assert len(Node.nodes.all()) == 6
        assert len(Node.nodes.filter(name='a')) == 1
        assert len(Node.nodes.filter(name='b')) == 1
        assert len(Node.nodes.filter(name='c')) == 1
        assert len(Node.nodes.filter(name='d')) == 1
        assert len(Node.nodes.filter(name='e')) == 1
        assert len(Node.nodes.filter(name='f')) == 1
        
        a = Node.nodes.get(name='a')
        b = Node.nodes.get(name='b')
        c = Node.nodes.get(name='c')
        d = Node.nodes.get(name='d')
        e = Node.nodes.get(name='e')
        f = Node.nodes.get(name='f')

        assert len(a.connections) == 0
        assert len(b.connections) == 0
        assert len(c.connections) == 0
        assert len(d.connections) == 0
        assert len(e.connections) == 0
        assert len(f.connections) == 0

        # Test API end point
        response = self.client.post('/node/connect/a/b')
        assert response.status_code == 200
        response = response.json()
        assert response is True
        
        assert len(Node.nodes.all()) == 6
        assert len(Node.nodes.filter(name='a')) == 1
        assert len(Node.nodes.filter(name='b')) == 1
        assert len(Node.nodes.filter(name='c')) == 1
        assert len(Node.nodes.filter(name='d')) == 1
        assert len(Node.nodes.filter(name='e')) == 1
        assert len(Node.nodes.filter(name='f')) == 1
        
        a = Node.nodes.get(name='a')
        b = Node.nodes.get(name='b')
        c = Node.nodes.get(name='c')
        d = Node.nodes.get(name='d')
        e = Node.nodes.get(name='e')
        f = Node.nodes.get(name='f')

        assert len(a.connections) == 1
        assert len(b.connections) == 0
        assert len(c.connections) == 0
        assert len(d.connections) == 0
        assert len(e.connections) == 0
        assert len(f.connections) == 0

        assert a.connections[0].name == 'b'

        # b to a
        response = self.client.post('/node/connect/b/a')
        assert response.status_code == 200
        response = response.json()
        assert response is True

        assert len(Node.nodes.all()) == 6
        assert len(Node.nodes.filter(name='a')) == 1
        assert len(Node.nodes.filter(name='b')) == 1
        assert len(Node.nodes.filter(name='c')) == 1
        assert len(Node.nodes.filter(name='d')) == 1
        assert len(Node.nodes.filter(name='e')) == 1
        assert len(Node.nodes.filter(name='f')) == 1
        
        a = Node.nodes.get(name='a')
        b = Node.nodes.get(name='b')
        c = Node.nodes.get(name='c')
        d = Node.nodes.get(name='d')
        e = Node.nodes.get(name='e')
        f = Node.nodes.get(name='f')

        assert len(a.connections) == 1
        assert len(b.connections) == 1
        assert len(c.connections) == 0
        assert len(d.connections) == 0
        assert len(e.connections) == 0
        assert len(f.connections) == 0

        assert a.connections[0].name == 'b'
        assert b.connections[0].name == 'a'

        # Test not found
        response = self.client.post('/node/connect/g/a')
        assert response.status_code == 404
        response = response.content
        assert response == b'g'

        response = self.client.post('/node/connect/a/h')
        assert response.status_code == 404
        response = response.content
        assert response == b'h'

        assert len(Node.nodes.all()) == 6
        assert len(Node.nodes.filter(name='a')) == 1
        assert len(Node.nodes.filter(name='b')) == 1
        assert len(Node.nodes.filter(name='c')) == 1
        assert len(Node.nodes.filter(name='d')) == 1
        assert len(Node.nodes.filter(name='e')) == 1
        assert len(Node.nodes.filter(name='f')) == 1
        
        a = Node.nodes.get(name='a')
        b = Node.nodes.get(name='b')
        c = Node.nodes.get(name='c')
        d = Node.nodes.get(name='d')
        e = Node.nodes.get(name='e')
        f = Node.nodes.get(name='f')

        assert len(a.connections) == 1
        assert len(b.connections) == 1
        assert len(c.connections) == 0
        assert len(d.connections) == 0
        assert len(e.connections) == 0
        assert len(f.connections) == 0

        assert a.connections[0].name == 'b'
        assert b.connections[0].name == 'a'

        # one more time a to b
        response = self.client.post('/node/connect/a/b')
        assert response.status_code == 200
        response = response.json()
        assert response is True

        assert len(Node.nodes.all()) == 6
        assert len(Node.nodes.filter(name='a')) == 1
        assert len(Node.nodes.filter(name='b')) == 1
        assert len(Node.nodes.filter(name='c')) == 1
        assert len(Node.nodes.filter(name='d')) == 1
        assert len(Node.nodes.filter(name='e')) == 1
        assert len(Node.nodes.filter(name='f')) == 1
        
        a = Node.nodes.get(name='a')
        b = Node.nodes.get(name='b')
        c = Node.nodes.get(name='c')
        d = Node.nodes.get(name='d')
        e = Node.nodes.get(name='e')
        f = Node.nodes.get(name='f')

        assert len(a.connections) == 1
        assert len(b.connections) == 1
        assert len(c.connections) == 0
        assert len(d.connections) == 0
        assert len(e.connections) == 0
        assert len(f.connections) == 0

    def test_path(self):
        """
        Test Shortest path
        """
        # create nodes

        a = Node(name='a').save()
        b = Node(name='b').save()
        c = Node(name='c').save()
        d = Node(name='d').save()
        e = Node(name='e').save()
        f = Node(name='f').save()
        g = Node(name='g').save()
        h = Node(name='h').save()
        i = Node(name='i').save()
        j = Node(name='j').save()
        k = Node(name='k').save()
        l = Node(name='l').save()
        m = Node(name='m').save()
        n = Node(name='n').save()

        # a -> b -> c -> d -> e -> f -> g -> h -> i
        # longest path
        a.connections.connect(b)
        b.connections.connect(c)
        c.connections.connect(d)
        d.connections.connect(e)
        e.connections.connect(f)
        f.connections.connect(g)
        g.connections.connect(h)
        h.connections.connect(i)

        # a -> j -> k -> l -> m -> i
        # another long path
        a.connections.connect(j)
        j.connections.connect(k)
        k.connections.connect(l)
        l.connections.connect(m)
        m.connections.connect(i)
        
        # a -> b -> c -> n -> i
        # shortest path
        c.connections.connect(n)
        n.connections.connect(i)

        # we should get 'A,B,C,N,I'
        response = self.client.get('/node/path/a/i')
        assert response.status_code == 200
        response = response.json()
        assert 'Path' in response
        path = response['Path']
        assert path.lower() == 'a,b,c,n,i'

        # disconnect c & n now we should get  a -> j -> k -> l -> m -> i
        c.connections.disconnect(n)
        response = self.client.get('/node/path/a/i')
        assert response.status_code == 200
        response = response.json()
        assert 'Path' in response
        path = response['Path']
        assert path.lower() == 'a,j,k,l,m,i'

        # connect n to e : # a -> b -> c -> d -> e -> n -> i
        # we still obtain previous result
        e.connections.connect(n)
        response = self.client.get('/node/path/a/i')
        assert response.status_code == 200
        response = response.json()
        assert 'Path' in response
        path = response['Path']
        assert path.lower() == 'a,j,k,l,m,i'

        # disconnect n & e 
        # connect n to d 
        # a -> b -> c -> d -> n -> i
        # now we have 2 shortest paths 
        # a -> b -> c -> d -> n -> i  &
        # a -> j -> k -> l -> m -> i
        
        e.connections.disconnect(n)
        d.connections.connect(n)
        response = self.client.get('/node/path/a/i')
        assert response.status_code == 200
        response = response.json()
        assert 'Path' in response
        path = response['Path']

        assert path.lower() == 'a,j,k,l,m,i'or path.lower() == 'a,b,c,d,n,i'
        # disconect k, l
        # now a -> b -> c -> d -> n -> i is the shortest
        k.connections.disconnect(l)
        response = self.client.get('/node/path/a/i')
        assert response.status_code == 200
        response = response.json()
        assert 'Path' in response
        path = response['Path']
        assert path.lower() == 'a,b,c,d,n,i'

        # no shortest path when start and end are the same
        response = self.client.get('/node/path/a/a')
        assert response.status_code == 404

        # no shortest path when start/end does not exist
        response = self.client.get('/node/path/a/x')
        assert response.status_code == 404
        response = self.client.get('/node/path/x/a')
        assert response.status_code == 404
        response = self.client.get('/node/path/x/z')
        assert response.status_code == 404
        
        # only get method is allowed

        response = self.client.post('/node/path/a/i')
        assert response.status_code == 405

        response = self.client.head('/node/path/a/i')
        assert response.status_code == 405

        response = self.client.put('/node/path/a/i')
        assert response.status_code == 405

        