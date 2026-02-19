# Prompt Customization Guide

This document explains where and how to customize the prompts sent to the AI.

## Where Prompts Are Located

All prompts are in `backend/main.py`:

1. **Classification Prompt** (line ~208): Determines workspace type
2. **Schema Generation Prompt** (line ~268): Creates workspace layout
3. **Suggestions Generation Prompt** (line ~366): Generates AI suggestions

## Current Prompts

### 1. Classification Prompt

**Location**: `classify_query()` function

**Purpose**: Accurately classify user queries into workspace types, especially distinguishing travel queries from other types.

**System Prompt**:
```
You are a query classifier for a research workspace application called Atlas. 
Analyze the user's search query and classify it into the most appropriate workspace type.

Workspace Types:
- travel_research: For queries about trips, vacations, travel destinations, itineraries, hotels, flights, restaurants, tourist attractions, travel planning
- purchase_research: For queries about buying products, comparing items, product reviews, specifications, prices, recommendations
- learning_plan: For queries about learning skills, courses, tutorials, study plans, educational resources, curriculum
- project_planner: For queries about planning projects, organizing tasks, project management, general planning

Examples:
- "plan a trip to japan" → travel_research
- "best laptop for coding" → purchase_research  
- "learn React in 4 weeks" → learning_plan
- "organize my startup idea" → project_planner
```

**User Prompt**:
```
Analyze this search query and classify it:
"{user_query}"

What type of research workspace does this query need?
```

**To Customize**: Edit the `system_prompt` and `user_prompt` variables in the `classify_query()` function.

### 2. Schema Generation Prompt

**Location**: `generate_schema()` function

**System Prompt**:
```
You are a workspace schema generator. Return ONLY valid JSON, no other text.
Return JSON format:
{
  "title": "Workspace Title",
  "modules": [{"type": "sources_panel"}, ...],
  "recommended_sources": ["web", "reddit", "youtube", "maps", "academic"],
  "source_queries": {
    "maps": ["query1", "query2"],
    ...
  }
}
```

**User Prompt**:
```
Query: "{user_query}"
Workspace Type: {workspace_type}

Generate a workspace schema with appropriate modules and source queries for this query.
```

**To Customize**: Edit the `system_prompt` and `user_prompt` variables in the `generate_schema()` function.

### 3. Suggestions Generation Prompt

**Location**: `generate_suggestions()` function

**Purpose**: Generate Google-search-like, relevant suggestions with real-world resources (travel guides, review sites, etc.) instead of generic workplace links.

**System Prompt**:
```
You are a research assistant for Atlas, a search engine that generates research workspaces.
Your job is to suggest relevant, high-quality resources that help users research their query - similar to what Google Search would return.

Generate 4-6 suggestions that are:
- Highly relevant to the user's query
- From reputable, well-known sources (like travel guides, review sites, official resources)
- Similar to top Google Search results for the query
- Actionable and useful for research

Guidelines:
- For travel queries: Suggest travel guides (Lonely Planet, TripAdvisor, official tourism sites), booking sites, travel blogs, Reddit communities
- For purchase queries: Suggest review sites (Wirecutter, Consumer Reports), comparison sites, official product pages, user forums
- For learning queries: Suggest educational platforms (Coursera, freeCodeCamp), official documentation, tutorial sites, learning communities
- Use realistic, well-known website names and URLs
- Make evidence sources diverse (mix of web, reddit, youtube when appropriate)
- Do NOT suggest workplace/office tools unless the query is explicitly about work/projects
- Focus on resources that would appear in top Google Search results
```

**User Prompt**:
```
User Query: "{user_query}"
Workspace Type: {workspace_type}

Generate 4-6 research suggestions that would help someone researching this query. 
Think: "What are the top resources someone would find if they Googled this query?"

For example, if the query is "plan a trip to japan", suggest:
- Official Japan tourism websites
- Popular travel guide sites (Lonely Planet, TripAdvisor)
- Travel booking platforms
- Reddit communities (r/JapanTravel)
- YouTube travel channels
- Travel blogs with Japan itineraries

Make suggestions specific, relevant, and from well-known sources. Include evidence links that represent the types of resources users would actually find.
```

**To Customize**: Edit the `system_prompt` and `user_prompt` variables in the `generate_suggestions()` function.

## Example: Adding More Context

You can add additional context to any prompt. For example, to add user preferences:

```python
user_prompt = f"""Query: "{request.query}"
Workspace Type: {workspace_type}
User Context: Focus on budget-friendly options and user reviews.

Generate evidence-linked suggestions that help the user research this query. Include 3-5 suggestions with evidence sources."""
```

## Viewing Prompts in Action

The code now logs all prompts being sent. Check your backend terminal output to see:
- System instruction
- User prompt  
- Full combined prompt

Look for lines starting with `=== PROMPT SENT TO AI ===` in your terminal.

## Tips

1. **Be specific**: More detailed prompts = better results
2. **Maintain JSON format**: Keep the JSON structure requirements in system prompts
3. **Test incrementally**: Change one prompt at a time to see the effect
4. **Check logs**: The terminal will show exactly what's being sent
