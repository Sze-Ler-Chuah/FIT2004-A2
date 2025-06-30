import math

#Quetion 1

class Node:
    def __init__(self,data=[None,0]):
        """
        Function description:
            init function is used to initialise a Node object. 

        :Input:
            data : The payload of node.  
                   It is a list which consists of 2 elements, 1st element is the definition of the word, 2nd element is the frequency of the word.
                   The default value being initialised is [None,0]
            
        :args:
            self.link : A list of 27 elements, each element is a pointer to another Node object.
            self.definition : The definition of the word.
            self.frequency : The frequency of the word.
            self.next_word_highest_freq_index : The index of the next character in the word with the highest frequency.
            self.current_max_frequency : While traversing along the word, this variable stores the current maximum frequency of the word prior reaching the terminal node.
            self.unique_freq : The number of unique words that starts with the same prefix.

        :Output, return or postcondition:
            None

        :Time complexity: O(1) Only initialisation 

        :Aux space complexity: O(1) No extra memory is used here
        """
        self.link = [None]*27
        self.definition = data[0]
        self.frequency = data[1]
        self.next_word_highest_freq_index = 0
        self.current_max_frequency = -1
        self.unique_freq = 0

class Trie:        
    def __init__(self, dictionary:list[tuple[str,str,int]]) -> None:
        """
        Function description:
            init function is used to initialise a Trie. 

        :Input:
            dictionary : A list of tuples, each tuple consists of 3 elements, 1st element is the word, 2nd element is the definition of the word, 
                         3rd element is the frequency of the word.
            
        :args:
            self.root : A Node object which is the root of the Trie.

        :Output, return or postcondition:
            A for loop is used to iterate through the dictionary, and insert each word into the Trie accordingly.

        :Time complexity: O(T), T is the total number of characters in the dictionary, each word's character is visited once

        :Aux space complexity: O(T), T is the total number of characters in the dictionary
        """
        self.root = Node()
        for data in dictionary:
            self.insert(data[0],data)

    def info_update(self,curr:Node,index:int,frequency:int) -> None:
        """
        Function description:
            info_update function is used to update the information of the node, ensuring the link to the next node is always the character with the highest frequency.

        Approach description (if main function):
            Each time this function is being used, it indicates that a new unique word is being inserted into the Trie.
            We decide whether to update the current_max_frequency and next_word_highest_freq_index of the current node based on 2 conditions below:
                (1) The frequency of the new word is higher than the current_max_frequency of the current node.
                (2) The frequency of the new word is the same as the current_max_frequency of the current node, 
                    but the index of the new word is smaller than the next_word_highest_freq_index of the current node.
            unique_freq of the current node is incremented by 1.
            
        :Input:
            curr : The current node.
            index : The index of the character in the word.
            frequency : The frequency of the word.
            
        :args:
            None

        :Output, return or postcondition:
           None

        :Time complexity: O(1)

        :Aux space complexity: O(1)
        """
        if (curr.current_max_frequency == frequency and curr.next_word_highest_freq_index > index) or curr.current_max_frequency < frequency:
            curr.current_max_frequency = frequency
            curr.next_word_highest_freq_index = index
        curr.unique_freq += 1

    def insert(self, key:str, data:list[str,str,int]=None) -> None:
        """
        Function description:
            insert function is used to insert words into the Trie character by character.
            
        Approach description (if main function):
           (i)  Initialise variable current with the value of self.root.
           
           (ii) Iterate through each character in the word, and insert the character into the Trie accordingly.
                (i) If current.link[index] is not None, which indicates there is already words which consits of the same prefix,
                    thus, we update the information of the current node and set current to link to next node.
                (ii) If current.link[index] is None, which indicates there is no words which consits of the same prefix,
                    thus, we create a new node and set current to link to next node.
                    
            (iii) Once we arrive at the terminal node, loop terminates and we start to check whether the current node has a link to the terminal node.
                (i) If current.link[index] is not None, which indicates there is already a word which consits of the same prefix,
                    thus, we update the information of the current node. 
                (ii) If current.link[index] is None, which indicates there is no word which consits of the same prefix,
                     thus, we create a new node and set current to link to next node.
            
        :Input:
            argv1 : key : The word to be inserted into the Trie character by character.
            argv2 : data : A list which consists of 3 elements, 1st element is the word, 2nd element is the definition of the word, 3rd element is the frequency of the word.
                           The default value is initialised as None.
            
        :args:
            None

        :Output, return or postcondition:
           None

        :Time complexity: O(length), length is the length of the word as the loop iterates through each letter in the word

        :Aux space complexity: 
            Best Case : O(definiton), definition as the number of letters of the definition of the word.
                        When there the word is already initialised in Trie, creating terminal node with the definiton of the word
                        is the only thing we do.
            Worst Case : O(definition + length), length as length of the word, definition as then number of letters of the definition of the word.
                         When the prefix of the word is new to to Trie, we will need to create a node for each letter 
        """
        #(i)
        current = self.root
        
        #(ii)
        for char in key:
            index = ord(char) - 97 + 1
            if current.link[index] is not None:
                self.info_update(current,index,data[2])
                current = current.link[index]
            else:
                current.link[index]=Node()
                self.info_update(current,index,data[2])
                current = current.link[index]
        #(iii)        
        index = 0
        if current.link[index] is None:
            current.link[index] = Node([data[1],data[2]])
            self.info_update(current,index,data[2])
        else:
            self.info_update(current,index,data[2])
            if current.current_max_frequency <= data[2]:
                current.link[index] = Node([data[1],data[2]])

    def prefix_search(self,prefix : str) -> list[str,str,int]:
        """
        Function description:
            prefix_search function is used to search for the word with the prefix given which has the highest frequency in the Trie 
            
        Approach description (if main function):
            (i) Initialse variable final_word with the value of prefix (Final word must starts with the prefix given)
                Initialise variable current with the value of self.root.
                Time Complexity: O(1) Initialisation only
                Aux Space Complexity: O(1) No extra memory is used here
                
            (ii) For loop is then used to iterate through each character in the prefix which below 2 conditions
                (i) If current.link[index] is None, which indicates there is no words which consits of the prefix given,
                    thus, we return [None,None,0]
                (ii) Else, we set current to link to next node.
                This help us to set up to further action of searching for the word with the prefix given which has the highest frequency in the Trie.
                Time Complexity: O(M), M is the length of the prefix
                Aux Space Complexity: O(M) No extra memory is used here
            
            (iii) Initialise variable final_unique_frequency with the value of current.unique_freq (The number of unique words that starts with the prefix given)
                  While loop is then used to search for the word with the prefix given which has the highest frequency in the Trie.
                  While current.definition is None (Only terminal node has definition), if current.next_word_highest_freq_index > 0, 
                  which indicates there is still an alphabet in the word with the highest frequency, we append the alphabet to final_word.
                  Then we set current to link to next node.
                  Loop terminates once we arrive at the terminal node and the word with the highest frequency is found along with its definition.
                  Return our final answer which is a list of 3 elements with the word with the highest frequency, its definition and the number of unique words that starts with the prefix given.
                  Time Complexity: O(N), N is the number of characters in the word with the highest frequency
                  Space Complexity: O(N), N is the number of characters in the word with the highest frequency
                 
        :Input:
            argv1 : prefix : The prefix of the word to be searched.
            
        :args:
            None

        :Output, return or postcondition:
            A list which consists of 3 elements, 
            1st element is the word with the highest frequency among the words which starts with the prefix given
            (If there are >= 1 words with the same highest frequency, the words which is lexigraphically smaller will be chosen) 
            2nd element is the definition of the word, 
            3rd element is the number of unique words that starts with the prefix given.
            
        :Time complexity: O(M) + O(N) = O(M+N)

        :Aux space complexity: O(M) + O(N) = O(M+N)
        """
        
        #(i)
        final_word = prefix
        current = self.root
        
        #(ii)
        for char in prefix:
            index = ord(char) - 97 + 1
            if current.link[index] is None:
                return [None,None,0]
            current = current.link[index]
         
         #(iii)       
        final_unique_frequency = current.unique_freq
        
        while current.definition is None:
            if current.next_word_highest_freq_index > 0:
                final_word += chr(current.next_word_highest_freq_index+96) 
            current = current.link[current.next_word_highest_freq_index]

        return [final_word,current.definition,final_unique_frequency]
    
### DO NOT CHANGE THIS FUNCTION
def load_dictionary(filename):
    infile = open(filename)
    word, frequency = "", 0
    aList = []
    for line in infile:
        line.strip()
        if line[0:4] == "word":
            line = line.replace("word: ","")
            line = line.strip()
            word = line            
        elif line[0:4] == "freq":
            line = line.replace("frequency: ","")
            frequency = int(line)
        elif line[0:4] == "defi":
            index = len(aList)
            line = line.replace("definition: ","")
            definition = line.replace("\n","")
            aList.append([word,definition,frequency])

    return aList

#Question 2
from collections import deque

class Vertex:
    def __init__(self,id:int) -> None:
        """
        Function description:
            init function is used to initialize the vertex object which represents each vertex in the graph

        :Input:
            id: the id of vertex ( Used to differentiate each vertex )
            
        :Instances:
            self.id: the id of vertex ( Used to differentiate each vertex )
            self.edges: the list of edges that are connected to the vertex
            self.discovered: a boolean value to indicate whether the vertex has been discovered or not
            self.visited: a boolean value to indicate whether the vertex has been visited or not
            self.previous: the previous edge that is used to reach this vertex

        :Output, return or postcondition:
            None

        :Time complexity: O(1) Initialisation 

        :Aux space complexity: O(1) No extra memory is used here
        """
        self.id = id
        self.edges = []
        self.discovered = False
        self.visited = False
        self.previous = None

class Edge:
    def __init__(self, u:int, v:int, f:int = 0, c:int = 0) -> None:
        """
        Function description:
            init function is used to initialize the edge object which represents each edge in the graph

        :Input:
            u: the vertex which is the departure point of the edge
            v: the vertex which is the arrival point of the edge
            f: the flow of the edge
            c: the capacity of the edge
            
        :Instances:
            self.depart: the vertex which is the departure point of the edge
            self.arrive: the vertex which is the arrival point of the edge
            self.flow : the flow of the edge
            self.capacity: the capacity (Maximum flow which can pass through) of the edge
            self.origin : One way edge (depart -> arrive) which created at FlowGraph
            self.front : One of the two-way edge (depart -> arrive) which created at residualNetwork
            self.behind : One of the two-way edge (arrive -> depart) which created at residualNetwork

        :Output, return or postcondition:
            None

        :Time complexity: O(1) Initialisation 

        :Aux space complexity: O(1) No extra memory is used here
        """
        self.depart = u 
        self.arrive = v
        self.flow = f
        self.capacity = c
        self.origin = None
        self.front = None
        self.behind = None
    
    def flow_augment(self, flow:int) -> None:
        """
        Function description:
            flow_augment is used to update the flow of the edge once a path is found 

        :Input:
            flow : the flow that which will be updated to the edge

        :Output, return or postcondition:
            None

        :Time complexity: O(1) Updating the flow of the edge, which is a constant time operation 

        :Aux space complexity: O(1) No extra memory is used here, only updating the flow of the edge
        """
        self.flow += flow
    
    def starting_point (self, edge:'Edge') -> 'Edge' :
        """
        Function description:
            starting_point is used to set up a pointer at flowGraph which represents the current edge

        :Input:
            edge : The edge of flowGraph to the current edge

        :Output, return or postcondition:
            The updated current edge will be returned

        :Time complexity: O(1) 

        :Aux space complexity: O(1) No extra memory is used here
        """
        self.origin = edge
        return self
    
    def residue_front (self,edge) :
        """
        Function description:
            residue_front is used to set up a pointer to the front edge of the current edge at residualNetwork

        :Input:
            edge : The forward edge to the current edge

        :Output, return or postcondition:
            The updated current edge will be returned

        :Time complexity: O(1) 

        :Aux space complexity: O(1) No extra memory is used here
        """
        self.front = edge
        return self
    
    def residue_behind (self,edge) :
        """
        Function description:
            residue_behind is used to set up a pointer to the behind edge of the current edge at residualNetwork

        :Input:
            edge : The behind edge to the current edge

        :Output, return or postcondition:
            The updated current edge will be returned

        :Time complexity: O(1) 

        :Aux space complexity: O(1) No extra memory is used here
        """
        self.behind = edge
        return self

class FlowGraph:
    def __init__ (self, sources:list[int], sinks:list[int], vertices:int) -> None:
        """
        Function description:
            init function is used to initialize the FlowGraph object which represents the circulation network with demnad

        :Input:
            sources : The list of sources in the circulation network with demand
            sinks : The list of sinks in the circulation network with demand
            vertices : The number of vertices in the circulation network with demand
            
        :Instances:
            self.sources : The list of sources in the circulation network with demand
            self.sinks : The list of sinks in the circulation network with demand
            self.super_source : The initialised position for super source in flowGraph
            self.super_sink : The initialised position for super sink in flowGraph
            self.vertices : The list of vertices in the FlowGraph
            self.residual_network : The residual network of the FlowGraph
            self.people : The number of people in the circulation network with demand
            self.edgesToSuperSink : The list of edges that are connected to the super sink

        :Output, return or postcondition:
            None

        :Time complexity: O(V + 2) = O(V), V as the number of vertices in the FlowGraph, iterating through all vertices once

        :Aux space complexity: O(2V+4) = O(V), V as the number of vertices in the FlowGraph, create FlowGraph and residualNetwork
        """
        self.sources = sources
        self.sinks = sinks
        self.super_source = vertices #Super Source
        self.super_sink = vertices + 1 #Super Sink
        self.vertices = [None]*(vertices + 2)
        for i in range(vertices + 2):
            self.vertices[i] = Vertex(i)
        self.residual_network = ResidualNetwork(vertices, self)
        self.people = None 
        self.edgesToSuperSink = []
    
    def superSource (self) -> None:
        """
        Function description:
            superSource is used to initialise the super source in the FlowGraph which allows Ford Fulkerson algorithm to work
            
        Approach description (if main function):
            (i)     First, initialise a variable total_people to store the total number of people in the circulation network with demand
                    (Based on the circulation with demand initialised, number of people can be found at self.sinks[1])
                    Time Complexity : O(1), accessing value in list is a constant time operation
                    Space Complexity : O(1), no extra memory is used here
                    
            (ii)    A for loop is then used to connect the super source to all the sources in the circulation network with demand.
                    By doing so, lower bound for license vertex to distance vertex will be eliminated, demand for license vertex will be set 
                    to 2 while the demand for distance vertex will be set to -2. 
                    Super source will be linked to destination vertex with demand of 2 
                    Then, the edges that are connected to the super sink will be stored in the list edgesToSuperSink
                    Time Complexity : O(2V), V as the number of vertices. 
                                      Super source is connect to all sources in Circulation with demand and all edges that are connected to the super sink
                                      is appended to the list edgesToSuperSink
                    Space Complexity : O(2V), V as the number of vertices.
                                       It is used to store the edges which are newly addded to FlowGraph and the edges that are connected to the super sink
                    
            (iii)   Finally, the super source will be connected to the source which the size of total_people as demand
                    Time Complexity : O(1), adding an edge from super source to one of the source in circulation with demand is a constant time operation
                    Space Complexity : O(1), no extra memory is used here

        :Input:
            None
            
        :Instances:
            None

        :Output, return or postcondition:
            Super source is added into the FlowGraph

        :Time complexity: O(2V + 2) = O(V)

        :Aux space complexity: O(2V + 2) = O(V)
        """
        #(i)
        total_people = self.sinks[1]
        
        #(ii)
        for i in range(1,len(self.sources)):
            self.formEdge(self.super_source, self.sources[i], 2, False)
            self.edgesToSuperSink.append(self.vertices[self.sources[i]].edges[-1])
        
        #(iii)    
        self.formEdge(self.super_source, self.sources[0], total_people, False)
    
    def superSink (self):
        """
        Function description:
            superSink is used to initialise the super sink in the FlowGraph which allows Ford Fulkerson algorithm to work
            
        
        Approach description (if main function):
            (i)     First, initialise a variable total_people to store the total number of people in the circulation network with demand
                    (Based on the circulation with demand initialised, number of people can be found at self.sinks[1])
                    Time Complexity : O(1), accessing value in list is a constant time operation
                    Space Complexity : O(1), no extra memory is used here
                    
            (ii)    A for loop is then used to connect all the license vertex to super_sink in the circulation network with demand.
                    By doing so, lower bound for license vertex to distance vertex will be eliminated, demand for license vertex will be set 
                    to 2 while the demand for distance vertex will be set to -2. 
                    License vertex will be linked to super sink with demand of 2 
                    Then, the edges that are connected to the super sink will be stored in the list edgesToSuperSink
                    Time Complexity : O(2V), V as the number of vertices. 
                                      License vertex is connected to super sink in Circulation with demand and all edges that are connected to the super sink
                                      is appended to the list edgesToSuperSink
                    Space Complexity : O(2V), V as the number of vertices.
                                       It is used to store the edges which are newly addded to FlowGraph and the edges that are connected to the super sink
                    
            (iii)   Super source will be connected to the source which the size of total_people as demand
                    Time Complexity : O(1), adding an edge from super source to one of the source in circulation with demand is a constant time operation
                    Space Complexity : O(1), no extra memory is used here
            
            (iv)    Finally, self.people will be updated to the total number of people in the circulation network with demand
                    Time Complexity : O(1), updating the value of self.people is a constant time operation
                    Space Complexity : O(1), no extra memory is used here

        :Input:
            None
            
        :Instances:
            None

        :Output, return or postcondition:
            Super source is added into the FlowGraph

        :Time complexity: O(2V + 3) = O(V)

        :Aux space complexity: O(2V + 3) = O(V)
        """
        #(i)
        total_people = self.sinks[1]
        
        #(ii)
        for i in range(1,len(self.sinks)):
            self.formEdge(self.sinks[i], self.super_sink, 2, False)
            self.edgesToSuperSink.append(self.vertices[self.sinks[i]].edges[-1])
        
        #(iii)    
        self.formEdge(self.sinks[0], self.super_sink, total_people, False)
        
        #(iv)
        self.people = total_people
    
    def formEdge (self, depart:int, destination:int, capacity:int, backward:bool = True):
        """
        Function description:
            formEdge is used to form an edge between two vertices will be added into the FlowGraph and residualNetwork           
        
        Approach description (if main function):
            (i)     Initialise a variable origin which is an edge with flow = 0 and capacity = capacity
                    Then, append the origin to FlowGraph
                    Time Complexity : O(1), 
                    Space Complexity : O(1)
            
            (ii)    Initialise a variable residual_front which is an edge with flow = capacity and capacity = capacity
                    (Flow is at maximum capacity to determine the total flow which can pass through the edge)
                    Set the starting point of residual_front to origin
                    Then, append the residual_front to residualNetwork
                    Time Complexity : O(1)
                    Space Complexity : O(1)
            
            (iii)   If backward is True, initialise a variable residual_behind which is an edge with flow = 0 and capacity = capacity
                    (Flow is at 0 as currently there is no flow passing through the edge)
                    Implement some setup to ensure backward edge in residual network has reverse start and end
                    Then, append the residual_behind to residualNetwork
                    (Optional as some edges such as super source and super sink cannot be reversed)
                    Time Complexity : O(1)
                    Space Complexity : O(1)

        :Input:
            depart : the vertex which is the departure point of the edge
            destination : the vertex which is the arrival point of the edge
            capacity : the capacity of the edge
            backward : a boolean value to indicate whether the edge is a backward edge or not

        :Output, return or postcondition:
            Construct edges in FlowGraph and residualNetwork

        :Time complexity: O(1)

        :Aux space complexity: O(1)
        """
        #(i) Create edge for FlowGraph
        origin = Edge(depart, destination, c=capacity )
        self.vertices[depart].edges.append(origin)
        
        #(ii) Create front edge for residualNetwork
        residual_front = Edge(depart, destination, capacity, capacity)
        residual_front = residual_front.starting_point(origin)
        self.residual_network.vertices[depart].edges.append(residual_front)
        
        #(iii) Create behind edge for residualNetwork
        if backward == True:
            residual_behind = Edge(destination, depart, c=capacity)
            residual_behind = residual_behind.starting_point(origin)
            residual_behind = residual_behind.residue_front(residual_front)
            self.residual_network.vertices[destination].edges.append(residual_behind)
            self.residual_network.vertices[depart].edges[-1].residue_behind(residual_behind)

    def desired_destination(self) -> list[list[int]]:
        """
        Function description:
            desired_destination is used to find which destination each person is allocated to.        
        
        Approach description (if main function):
            (i)     Initialise a variable target which is used to store the value of a list of list which indicates which destination each person is allocated to.
                    Time Complexity : O(N), N as the number of people, itearting through all people once.
                    Space Complexity : O(N), N as the number of people, create a list of list to store the value of which destination each person is allocated to.
            
            (ii)    Nested for loop is used to iterate through all the edges that are connected to each person.
                    The edge which has flow of 1 indicates that the person is allocated to the destination which the edge is pointing to. 
                    Compute the vertex which the edge is pointing to and append it to the list which is stored in target
                    Time Complexity : O(N^2), N as the number of people, itearting through all people once and all edges that are connected to each person once.
                    Space Complexity : O(1), no extra memory is used here

        :Input:
            None

        :Output, return or postcondition:
            A list of list which indicates which destination each person is allocated to.

        :Time complexity: O(N + N^2) = O(N^2) (N^2 >> N)

        :Aux space complexity: O(N + 1) = O(N)
        """
        #(i)
        target = [[] for i in range(math.ceil(self.people/5))]
         
        #(ii)   
        for people in range(self.people):
            for selection in self.vertices[people].edges:
                if selection.flow == 1:
                    target[math.floor((selection.arrive-self.people)/2)].append(selection.depart)
                    
        return target
                
class ResidualNetwork:
    def __init__(self, vertices_count:int, graph:FlowGraph) -> None:
        """
        Function description:
            init function is used to initialize the ResidualNetwork object which represents the residual network of the FlowGraph

        :Input:
            vertices_count : the number of vertices in the residual network
            graph : Reference which is used to build the residual network
            
        :Instances:
            self.source : the super source of the residual network
            self.sink : the super sink of the residual network
            self.vertices : the list of vertices in the residual network
            self.path : the list of edges which is used to backtrack from sink to source
            self.pathAvailable : a boolean value to indicate whether there is a path from source to sink

        :Output, return or postcondition:
            None

        :Time complexity: O(V + 2) = O(V), V as the number of vertices in the residual network, iterating through all vertices once

        :Aux space complexity: O(V+2) = O(V), V as the number of vertices in the residual network
        """
        self.source = graph.super_source #Starts at super source
        self.sink = graph.super_sink #Ends at super sink
        self.vertices = [None]*(vertices_count + 2)
        for i in range(vertices_count + 2):
            self.vertices[i] = Vertex(i)
        self.path = []
        self.pathAvailable = False
    
    def bfs(self, source : Vertex) -> None:
        """
        Function description:
            bfs is used to find a valid path from source to sink in the residual network       
        
        Approach description (if main function):
            Initialise a variable discovered which is a deque to store the vertices that are discovered.
            Append the source to discovered.
            While loop is used to iterate through all the vertices that are discovered.
            (Which will be part of the path from source to sink)
            Pop the vertex which is at the end of the deque.
            Set the vertex as discovered and visited.
            If the vertex is the sink or there is a path from source to sink, break the loop.
            Else, for loop is used to iterate through all the edges that are connected to the vertex.
            Variable v is used to store the vertex which the edge is pointing to.
            If the vertex is not visited, not discovered and the flow of the edge is greater than 0,
            set the previous vertex v as the edge, set v as discovered and append v to discovered.
            If the vertex is the sink, set pathAvailable to True and break the loop.
            
            Time Complexity : O(V + E), V as the number of vertices, E as the number of edges, worst case where we iterate through all vertices and edges once
            Space Complexity : O(V), V as the number of vertices, create a deque to store the vertices that are discovered

        :Input:
            None

        :Output, return or postcondition:
            None

        :Time complexity: O(V + E), V as the number of vertices, E as the number of edges

        :Aux space complexity: O(V), V as the number of vertices
        """
        discovered = deque()
        discovered.append(source)
        while discovered:
            u = discovered.pop()
            u.discovered = True
            u.visited = True
            if u is self.sink or self.pathAvailable:
                break
            for edge in u.edges:
                v = self.vertices[edge.arrive]
                if v.visited is False:
                    if v.discovered is False:
                        if edge.flow > 0:
                            v.previous = edge
                            v.discovered = True
                            discovered.append(v)
                            if edge.arrive is self.sink:
                                self.pathAvailable = True
                                break
                    
    def backTrack(self) -> int:
        """
        Function description:
            backTrack is used to backtrack from sink to source and find the flow that pass through the path from source to sink     

        :Input:
            None

        :Output, return or postcondition:
            Return the flow that pass through the path from source to sink

        :Time complexity: O(V), Worst case where we iterate through all vertices once

        :Aux space complexity: O(E), E as the number of edges, create a list to store the all edges that are connected to the path
        """
        self.path = [] #backtrack from sink to source
        backtrack_initial = self.vertices[self.sink]
        flow = math.inf
        while backtrack_initial != self.vertices[self.source]:
            self.path.append(backtrack_initial.previous)
            flow = min(backtrack_initial.previous.flow, flow)
            backtrack_initial = self.vertices[backtrack_initial.previous.depart]
        return flow

    def reset_state(self) -> None:
        """
        Function description:
            reset_stae is a function which helps to reset vertices property to initial state.
            Reason : To enable bfs to be used multiple times until there is no path from source to sink in the residual network
            It also set pathAvailable to False to indicate that there is no path from source to sink in the residual network
            Reason : This helps to find a new path when bfs is reused
            
        Approach description (if main function):
            First, a for loop is used to reset vertices property discovered,visited,previous.
            Then, set pathAvailable to False 
        
        :Input:
            None
        
        :Output, return or postcondition:
            None
            
        :Time complexity: O(V) All vertices are visited once 
        :Aux space complexity: O(1) No memory is used here
        """
        for i in self.vertices:
            i.visited = False
            i.discovered = False
            i.previous = None
        self.pathAvailable = False

    
    def update_flow(self, flow:int) -> None:
        """
        Function description:
            Update the flow of edges in the path from source to sink in the residual network and FlowGraph
        
        Approach description (if main function):
            A for loop is used to iterate through all the edges in the path.
            First, update the flow of the edge.
            Then, check whether the edge is a front edge or a behind edge.
            If the edge is a behind edge, 
            origin adge and the behind edge is being added with flow.
            If the edge is a front edge,
            origin edge is being added with flow and the front edge is being subtracted with flow.
            Else, origin edge is being added with flow.
            
        :Input:
            supply : the bottleneck along the path

        :Output, return or postcondition:
            None

        :Time complexity: O(E), E as the number of edges in the path, iterating through all edges in the path and update the flow of the edge
        
        :Aux space complexity: O(1), no extra memory is used here
        """
        for edge in self.path :
            #update the flow of the flowNetwork
            edge.flow_augment((-1)*flow)
            #update the flow of the residualNetwork
            if edge.behind != None:
                edge.origin.flow_augment(flow)
                edge.behind.flow_augment(flow)
                
            elif edge.front != None:
                edge.origin.flow_augment((-1)*flow)
                edge.front.flow_augment(flow)
            
            else:
                edge.origin.flow_augment(flow)

def weekend_gateaway (preferences:list[list[int]],licenses:list[int]) -> tuple[list[tuple[int,int,int]] , list[int] , list[int]]:
    """
    Function description:
        weekend_gateaway is used to build the circulation network with demand based on the preferences list and licenses list the question provided.
                
    Approach description (if main function):
        (i)     First we initialise vairiable total_people, initial_source, initial_sink, people_count, gateaway, each_preference, begin, terminate with 
                their initial value respectively.
                Then, we initialise vairiable license with the value of an array of False with the length of total_people to indicate all people do not have
                license initally.
                Time Complexity: O(N), N as the number of people, iterate through every people once.
                Space Complexity: O(N), N as the number of people, a list with size of N is created to record which people owns a license later. 
        
        (ii)    Then, iterate through the licenses list to update the license array to indicate which people owns a license.
                Time Complexity: O(N), N as the number of people, worst case where all people owns a license.
                Space Complexity: O(1), no extra memory is used here.
        
        (iii)   Append initial_source to begin (empty list) and initial_sink to terminate (empty list).
                Time Complexity: O(1)
                Space Complexity : O(2N), N as the number of people, create two list with size of N to store the value of list of sources and list of sinks.
        
        (iv)    A nested for loop is used to connect initial_source with all people and all people with having license vertex and not having license vertex.
                Initial source will be connected to all people with a capacity of 1, indicating the presence of the people who is joining the weekend gateaway.
                All people will be connected to either having license vertex or not having license vertex with a capacity of 1, indicating the people of having 
                a license or not. 
                
                Vertex 0 - Vertex total_people-1 indicate the total number of people who is joining the weekend gateaway.
                Vertex total_people + 2*j indicate the people who is having a license, j >= 0 && j <= total_people
                Vertex total_people + 2*j + 1 indicate the people who is not having a license, j >= 0 && j <= total_people
                
                Time Complexity : O(N^2), N as the number of people, connecting initial_source with all people once, connecting all people with having license vertex 
                                  or not having license vertex once. 
                Space Complexity : O(N + math.ceil(N/5)*N), N as the number of people, worst case where N edges will be formed from initial_source to all people,
                                   math.ceil(N/5)*N edges will be formed from all people to having license vertex and not having license vertex.
        
        (v)     A for loop is used to connect having license vertex and not having license vertex with destination vertex.
                Each having license vertex and not having license vertex will be connected to destination vertex with a capacity of 3, since there is a lower bound 2
                Destination vertex will be connected to initial_sink with a capacity of 5.

                Vertex total_people + 2*i indicate the people who is having a license, i >= 0 && i <= total_people
                Vertex total_people + 2*i + 1 indicate the people who is not having a license, i >= 0 && i <= total_people
                Vertex total_people + 2*math.ceil(total_people/5) + i indicate the destination vertex, i >= 0 && i <= math.ceil(total_people/5)
                
                Time Complexity : O(N), N as the number of people, connecting having license vertex and not having license vertex with destination vertex once, 
                                  connecting destination vertex to initial_sink once.
                Space Complexity : O(math.ceil(N/5)*2 + math.ceil(N/5)), N as the number of people, worst case where math.ceil(N/5)*2 edges will be formed from 
                                   having license vertex and not having license vertex to destination vertex, math.ceil(N/5) edges will be formed from destination
                                   vertex to initial_sink.
        
        (vi)    Initial_sink will be connected to initial_source with a capacity of math.ceil(N/5)*5 - N to form a circulation network with demand.
                Time Complexity : O(1)
                Space Complexity : O(1)
        
        (vii)   Return a tuple which contains below three item:
                (1)     gateaway: A list of edges for the circulation of network with demand where each edge 
                                contain a tuple which following item, first one, source, second one, destination, third one, capacity
                (2)     begin:  A list of sources which will be used at ford_fulkerson method later
                (3)     terminate : A list of sinks which will be used at ford_fulkerson method later
                
                Time Complexity : O(1)
                Space Complexity : O(1)

    :Input:
        preferences: The list of preferences of which destination to go for each people
        licenses: The list of licenses indicating which people owns a license

    :Output, return or postcondition:
        A tuple which contains below three item:
        (1)     gateaway: A list of edges for the circulation of network with demand where each edge 
                          contain a tuple which following item, first one, source, second one, destination, third one, capacity
        (2)     begin:  A list of sources which will be used at ford_fulkerson method later
        (3)     terminate : A list of sinks which will be used at ford_fulkerson method later

    :Time complexity: O(N + N + 1 + N^2 + N + 1 + 1) = O(3 + 3N + N^2) =  O(N^2), N as the number of people

    :Aux space complexity: O(N + 1 + 2N + N + math.ceil(N/5)*N + math.ceil(N/5)*2 + math.ceil(N/5) + 1 + 1) = O(N^2), N as the number of people 
    """
    #(i)
    total_people = len(preferences)
    initial_source = total_people+3*(math.ceil(total_people/5))
    initial_sink = initial_source + 1 
    people_count = 0
    gateaway = []
    each_preference = math.ceil(total_people/5)
    begin = []
    terminate = []
    license = [False]*total_people
    
    #(ii)
    for i in licenses:
        license[i] = True 
    
    #(iii)
    begin.append(initial_source)
    terminate.append(initial_sink)
    
    #(iv)
    for i in preferences:
        gateaway.append((initial_source,people_count,1))
        for j in i:
            if license[people_count] == False:
                no_license = total_people+2*j+1
                gateaway.append((people_count,no_license,1))
            else:
                have_license = total_people+2*j
                gateaway.append((people_count,have_license,1))
        people_count += 1
    
    #(v)
    for i in range(each_preference):
        have_license = total_people+2*i
        no_license = (total_people+2*i)+1
        destination = total_people+2*math.ceil(total_people/5)+i
        gateaway.append((have_license,destination,3))
        gateaway.append((no_license,destination,3))
        gateaway.append((destination,initial_sink,5))
        begin.append(destination)
        terminate.append(have_license)
    
    #(vi)
    gateaway.append((initial_sink,initial_source,math.ceil(total_people/5)*5 - total_people))
    
    #(vii)
    return (gateaway,begin,terminate)

def ford_fulkerson(begin:list[int], terminate:list[int], edge:list[tuple[int,int,int]]) -> FlowGraph:
    """
    Function description:
        ford_fulkerson is used to find the maximum flow by finding all path available from source to sink  
                
    Approach description (if main function):
        (i)     Initialise a variable currentMax to store the maximum number of vertices in the circulation network with demand
                A for loop is used to iterate through all the edges in the circulation network with demand to find the maximum number of vertices
                Time Complexity : O(E), E as the number of edges, iterating through all edges once
                Space Complexity : O(1), no extra memory is used here
        
        (ii)    Initialise a variable graph with the value of FlowGraph which is used to store the circulation network with demand
                Time Complexity : O(V), V as the number of vertices, iterating through all vertices once
                Space Complexity : O(V), V as the number of vertices, create a list to store the vertices in the circulation network with demand
        
        (iii)   A for loop is used to iterate through all the edges in the circulation network with demand to form edges in FlowGraph
                Time Complexity : O(E), E as the number of edges, iterating through all edges once
                Space Complexity : O(1), no extra memory is used here
        
        (iv)    Add super source and super sink into FlowGraph
                Time Complexity : O(2V) (Details at superSource and superSink)
                Space Complexity : O(2V) (Details at superSource and superSink)
        
        (v)     Run bfs in residualNetwork to find a path from super source to super sink
                Time Complexity : O(V + E), V as the number of vertices, E as the number of edges
                Space Complexity : O(V), V as the number of vertices, create a deque to store the vertices that are discovered
        
        (vi)    While residual network still has path from super source to super sink, run backTrack to find the flow that pass through the path
                Update the flow of edges in the path from source to sink in the residual network and FlowGraph
                Reset vertices property to initial state
                Run bfs in residualNetwork again to find a path from super source to super sink.
                Once there is no path left, return the current FlowGraph
                Time Complexity : O(M)*(O(V) + O(E) + O(V) + O(V+E)) = O(M*(V+E)) = O(MV + ME) = O(ME), E >> V, 
                                    M as the number of times bfs is runned, V as the number of vertices, E as the number of edges
                Space Complexity : O(M)*(O(1) + O(E) + O(V)) = O(E), V as the number of vertices, created when bfs is runned
        
        (vii)   Check whether s-t cut is a min cut and provides us with a maximum flow. O(N) O(1)
                If true, return a list of list which indicates which destination each person is allocated to.
                Else, return None
                Time Complexity : O(N + N^2) = O(N^2), N as the number of people (Details at check_feasibility and desired_destination)
                Space Complexity : O(N + 1) = O(N), N as the number of people (Details at check_feasibility and desired_destination)      

    :Input:
        begin : the list of vertices which are the sources in the circulation network with demand
        terminate : the list of vertices which are the sinks in the circulation network with demand
        edge : the list of edges in the circulation network with demand   

    :Output, return or postcondition:
        Return the FlowGraph when there is no more path, checking feasibility (whether the s-t cut is a min cut and max flow)
        and returning the desired location each people allocated to will be carried on later at allocate function. 

    :Time complexity: O(E + V + E + 2V + (E+V) + ME) = O(4E + 4V + ME) = O(ME), E >> V

    :Aux space complexity: O(1 + V + 1 + 2V + V + E) = O(4V + E) = O(V + E), E >> N, V >> N
    """
    #(i)
    currentMax = 0
    for i in edge:
        if i[0] > currentMax:
            currentMax = i[0]
        if i[1] > currentMax:
            currentMax = i[1]
    
    #(ii)        
    graph = FlowGraph(begin,terminate,currentMax+1)
    
    #(iii)
    for i in edge:
        graph.formEdge(i[0],i[1],i[2])
    
    #(iv)
    graph.superSource()
    graph.superSink()
    
    #(v)
    graph.residual_network.bfs(graph.residual_network.vertices[graph.super_source])
    
    #(vi)
    while graph.residual_network.pathAvailable:
        flow = graph.residual_network.backTrack()
        graph.residual_network.update_flow(flow)
        graph.residual_network.reset_state()
        graph.residual_network.bfs(graph.residual_network.vertices[graph.super_source])
        
    return graph

def allocate(preferences:list[list[int]],licenses:list[int]) -> list[list[int]] or None:
    """
    Function description:
        allocate function is used to allocate every people to their desired destination based on the preferences list and licenses list the question provided 
                
    Approach description (if main function):
        (i)     Initialise variable information with the value of building the circulation network with demand based on the preferences list and licenses list 
                the question provided using weekend_gateaway function.
                Time Complexity : O(N^2), N as the number of people (Details at weekend_gateaway function)
                Space Complexity : O(N^2), N as the number of people (Details at weekend_gateaway function)
        
        (ii)    Initialise variable graph with the value of ford_fulkerson function which is used to find the maximum flow.
                Time Complexity : O(ME), M as the number of bfs runned, E as the number of edges (Details at ford_fulkerson function)
                At here, M is actually  N + 2*math.ceil(N/5), E is actually N^2, thus Time Complexity will be updated to O(N^3)
                Space Complexity : O(V +E), V as the number of vertices, E as the number of edges (Details at ford_fulkerson function)
        
        (iii)   Check whether s-t cut is a min cut and provides us with a maximum flow.
                (i)     Initialise a varaible full_condition with the value which indicates the maximum flow
                        Initialise a variable outgoingFlow to store the total flow that is leaving the super source
                        Initialise a variable incomingFlow to store the total flow that is entering the super sink
                        Time Complexity : O(1)
                        Space Complexity : O(1)
            
                (ii)   For loop is then used to sum up all the flow that is leaving the super source
                        Time Complexity : O(N), N as the number of people, worst case where we iterate through all people once
                        Space Complexity : O(1)
            
                (iii)   For loop is then used to sum up all the flow that is entering the super sink
                        Time Complexity : O(N), N as the number of people, worst case where we iterate through all people once
                        Space Complexity : O(1)
        
                Overall Time Complexity : O(2N) = O(N), N as the number of people 
                Overall Space Complexity : O(3) = O(1), no extra memory is used here
        
        (iv)    If outgoingFlow == incomingFlow and outgoingFlow == full_condition,
                return the desired destination each people allocated to.
                Else, return None
                Time Complexity : O(N^2), N as the number of people (Details at desired_destination)
                Space Complexity : O(N), N as the number of people (Details at desired_destination)
        
    :Input:
        preferences: The list of preferences of which destination to go for each people
        licenses: The list of licenses indicating which people owns a license

    :Output, return or postcondition:
        Return a list of list which indicates which destination each person is allocated to or None if there is no solution.

    :Time complexity: O(N^2 + N^3 + N + N^2) = O(N^3), N as the number of people

    :Aux space complexity: O(N^2 + N^2 + 1 + N^2) = O(N^2), N as the number of people
    """
    #(i)
    information = weekend_gateaway(preferences,licenses)
    
    #(ii)
    graph = ford_fulkerson(information[1],information[2],information[0])
    
    #(iii)
    ##(iii.i)
    full_condition = graph.people + 2*math.ceil(graph.people/5)
    outgoingFlow = 0
    incomingFlow = 0
    
    ##(iii.ii)
    for edge in graph.vertices[graph.super_source].edges:
        outgoingFlow += edge.flow
    
    ##(iii.iii)
    for edge in graph.edgesToSuperSink:
        incomingFlow += edge.flow
    
    #(iv)
    if outgoingFlow == incomingFlow and outgoingFlow == full_condition:
        return graph.desired_destination()
    return None