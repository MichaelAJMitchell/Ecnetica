# Describing a proposed structure of the knowledge graph

### Example
```
    {
      "id": 0,
      "topic": "Pythagorean theorem application in right-angled triangles",
      "description": "Using the relation a² + b² = c² to solve problems involving lengths in right-angled triangles, including heights and distances"
      "chapter": "trigonometry",
      "dependencies": [[6,0.5],[14, 0.8],[15, 0.6]]
    },
```
## id
id is an index that corresponds to the index of the node is the basis. Every node is numbered sequentially from 0-whatever the number of nodes is.
This is used rather than uuids, as it is simpler. The benefit of uuids is for if parts o the knowledge graph are generated separately, as making sure indexes follow on and don't overlap would be tricky. Also adding nodes could be a problem with indexes, but if you added them add the end always it should be fine. But if we are generating the knowledge graph all at once then there shouldn't be a problem with using indexes over uuids.

## topic
the name of the actual topic the node corresponds to. 

## description
a more in depth explanation of what exactly the node corresponds too. 

## chapter
what chapter the node comes under. 
This is useful for clustering. This should roughly correspond to the chapters students would use in school, so that they are able to choose to study a chapter. A list could be directly created for this with all the possible chapters, rather than letting the llm automatically assign chapter, with it instead catagorising each topic into an already given chapter.

### node area (maybe)
We could possibly cluster the nodes at another level below chapters and store this information with each node too. This would correspond to an area within a chapter, such as trig -> trig graphs -> graph of sin(ax)

## dependencies
Edges in a list with index of node the edge goes to and the weight of the edge. 

An edge should exist when knowledge of a topic is directly required to progress to the next topic, eg power rule differentiation -> chain rule differentiation. Nodes that are already assumed knowledge for prerequisites should not be included, as they are implicitly included already. The only exception to this is when a topic is directly required to understand/ solve the topic in question. Eg solving quadratic equations is directly required for finding turing points of cubic functions, so it should be a direct prerequisite, even if it is already an indirect prerequisite. This means that when mastery is backpropagated to related nodes, topics explicitly used in the question receive a higher update. 

The weight of an edge is determined by how closely related two topics are. If they are very conceptually similar, ie the conceptual jump from one node to the next is small, then the weighting should be large. If the topics are not very similar (ie large conceptual jump between them, maybe with one topic much more fundamental than the next), then the weighting should be small. This means that mastery levels of one topic more directly predicts knowledge of the next. Mastering a necessary prerequisite such as basic algebra is necessary, but will not be very accurate at predicting ability for a more complex calculus topic. However a student being strong at a closely related topic means that they will most likely also be good at another. This also applies to backpropagating masteries, as the mastery of a much more closely related topic should get a higher mastery update than more conceptually distant topics. 

