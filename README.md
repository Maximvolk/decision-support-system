# Decision Support System

Basic structure implemented. There're three API methods:
1. /GetRecommendation: gets problem description in log or stdout text format
and returns recommendations sorted by relevance (rating).  
2. /RateRecommendation: get problem, recommendation and "did helped" flag
and tune problem->recommendation rating (compliance rating).  
3. /AddRecommendation: gets recommendation and saves it to knowledge base.  

API documentation is powered by OpenAPI Swagger.  
![](demo/swagger.png)