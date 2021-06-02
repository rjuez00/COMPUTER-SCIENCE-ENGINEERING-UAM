package testers;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import graphImplementation.Graph;
import graphImplementation.Node;

public class Tester1 {

	public static void main(String[] args) {
		Graph<String, Integer> g = new Graph<String, Integer>();
		Node<String> n1 = new Node<String>("s0");
		Node<String> n2 = new Node<String>("s1");
		g.addAll(Arrays.asList(n1, n2, n1)); // does not admit repetitions, considering referential equality
		g.connect(n1, 0, n1); // we connect n1 with n1 through an edge with value 0
		g.connect(n1, 1, n2);
		g.connect(n1, 0, n2);
		g.connect(n2, 0, n1);
		g.connect(n2, 1, n1);
		System.out.println(g); // The graph contains 2 nodes and 5 edges
		for (Node<String> n : g) // Collection of two nodes (n1 and n2)
			System.out.println("Node "+n);
		List<Node<String>> nodes = new ArrayList<>(g); // we can create a list from g
		System.out.println(nodes);
		// Two methods to check connectivity, the first receives the value of the Node
		System.out.println("s0 connected with ‘s1’: "+ n1.isConnectedTo("s1"));
		System.out.println("s0 connected with s1: "+ n1.isConnectedTo(n2));
		System.out.println("neighbours of s0: "+ n1.neighbours());
		System.out.println("value of the edges from s0 to s1: "+n1.getEdgeValues(n2));
	}

}

