# Describing the structure of the knowledge graph

### Example
```
    {
      "id": 0,
      "topic": "solving linear equations",
      "chapter": "algebra",
      "dependencies": [
        {"target": 6, "weight": 0.5},
        {"target": 14, "weight": 0.8},
        {"target": 15, "weight": 0.6}
      ]
    },
```
## id
id is an index that corresponds to the index of the node is the basis. Every node is numbered sequentially from 0-?.
This is used rather than uuids, as it is simpler. The benefit of uuids is for if parts the knowledge graph are generated separately, as making sure indexes follow on and don't overlap would be tricky. Also adding nodes could be a problem with indexes, but if you added them add the end always it should be fine. But if we are generating the knowledge graph all at once then there shouldn't be a problem with using indexes over uuids.

## topic
the name of the actual topic the node corresponds to. 

## description
a more in depth explanation of what exactly the node corresponds too. 

## chapter
what chapter the node comes under. 
This is useful for clustering. This should roughly correspond to the chapters students would use in school, so that they are able to choose to study a chapter. A list could be directly created for this with all the possible chapters, rather than letting the llm automatically assign chapter, with it instead catagorising each topic into an already given chapter.

### node area (maybe)
We could possibly cluster the nodes at another level below chapters and store this information with each node too. This would correspond to an area within a chapter, such as trig -> trig graphs -> graph of sin(ax)

## 