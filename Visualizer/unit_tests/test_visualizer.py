from unittest.mock import Mock, call, patch
from unittest import TestCase
from Visualizer.Visualizer import Visualizer

class TestVisualizer(TestCase):
    """ Tests the visualizer for party problems. """

    @patch('Visualizer.Visualizer.Subject.__init__')
    @patch('Visualizer.Visualizer.Observer.__init__')
    @patch('Visualizer.Visualizer.Visualizer._setup_eventhandlers')
    @patch('Visualizer.Visualizer.Builder')
    def test_init(self, builder_mock, handlers_mock, obs_mck, sub_mck):
        """ Tests the initialisation of the gui. """
        builder_mock.add_from_file = Mock()
        builder_mock.get_object = Mock()

        gui = Visualizer(None)  # Do the thing
        sub_mck.assert_called_with(gui)         # Ensure parent constructors are called.
        obs_mck.assert_called_with(gui)
        assert builder_mock.call_count == 1     # Ensure builder has been created.
        assert handlers_mock.call_count == 1    # Ensure event handlers have been added.

    @patch('Visualizer.Visualizer.Visualizer._notify_observers')
    @patch('Visualizer.Visualizer.Visualizer._validate_input')
    def test_btn_solve(self, validate_mock, notify_mock):
        """ Ensure action checks validation before notifying observers. """
        gui = Visualizer(None)

        validate_mock.return_value = True   # Try with valid input
        gui._btn_solve_press()
        assert notify_mock.call_count == 1

        validate_mock.return_value = False   # Try with invalid input
        gui._btn_solve_press()
        assert notify_mock.call_count == 1  # (Last test added one)
    
    def test_validate_input(self):
        """ Tests the validation of input. """
        gui = Visualizer(None)
        gui._builder.get_object = Mock()
        returnable = Mock()
        returnable.get = Mock()
        
        returnable.get.return_value = "Not valid" # Check error raised when invalid value is given
        gui._builder.get_object.return_value = returnable
        try:
            gui._validate_input()
            assert False
        except Exception:
            assert True
        
        returnable.get.return_value = "5" # Check no error raised when invalid value is given
        gui._builder.get_object.return_value = returnable
        try:
            result = gui._validate_input()
            assert result
        except Exception:
            assert False
    
    @patch('Visualizer.Visualizer.Visualizer._determine_colour')
    def test_draw_graph(self, det_col):
        """ Ensures a graph is drawn with the corredct items. """
        gui = Visualizer(None)
        fake_canvas = Mock()
        fake_canvas.create_oval = Mock()
        fake_canvas.create_line = Mock()
        gui._builder = Mock()
        gui._builder.get_object = Mock()
        gui._builder.get_object.return_value = fake_canvas

        # Test vertice drawing
        from Visualizer.Graphing.Graph import Graph
        from Visualizer.Graphing.Vertex import Vertex
        g = Graph() # Setup graph
        vertex_one = Vertex(0)
        g.add_vertex(vertex_one)
        g.add_vertex(Vertex(1))
        g.add_vertex(Vertex(2))
        gui._draw_graph(g)  # Try drawing
        assert fake_canvas.create_oval.call_count == 3

        # Test edge drawing
        from Visualizer.Graphing.Edge import Edge
        edge = Edge(0, vertex_one, vertex_one, colour=5)   # Setup (Continued from above)
        g.add_edge(edge)
        gui._draw_graph(g)   # Try drawing
        det_col.assert_called_with(5)
        assert fake_canvas.create_line.call_count == 1
    
    def test_determine_colour(self):
        """ Ensure colours are returned with the relevant values. """
        gui = Visualizer(None)
        assert gui._determine_colour(0) == 'red'
        assert gui._determine_colour(1) == 'green'
        assert gui._determine_colour(2) == 'cyan'
        assert gui._determine_colour(3) == 'blue'
        assert gui._determine_colour(500) == 'blue'

    def test_notifying_observers(self):
        """ Ensures the norifying of observers happens with the correct argument. """
        gui = Visualizer(None)

        observer = Mock()   # Setup with a fake observer
        observer.update = Mock()
        gui._observers = [observer]

        gui._builder.get_object = Mock()    # Setup fake values
        returnable = Mock()
        returnable.get = Mock()

        returnable.get.return_value = "999"   # Look for 999
        gui._builder.get_object.return_value = returnable
        gui._notify_observers()

        observer.update.assert_called_with({"clique_size": 999, "graph_size": 999})

    @patch('Visualizer.Visualizer.Visualizer._draw_graph')
    def test_update(self, draw_graph):
        """ Ensures the view updates if a graph is provided. """
        gui = Visualizer(None)
        args = {"graph": "GRAPH"}   # Try with a graph
        gui.update(args)
        draw_graph.assert_called_with("GRAPH")
        assert draw_graph.call_count == 1

        args = {}   # Try without a graph
        gui.update(args)
        assert draw_graph.call_count == 1   # (Continuing from previous test)