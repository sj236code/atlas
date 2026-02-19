"""
Atlas Backend - FastAPI server for workspace generation and AI orchestration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Support both GEMINI_MODEL and AI_MODEL env vars
GEMINI_MODEL = os.getenv("GEMINI_MODEL") or os.getenv("AI_MODEL") or "gemini-pro"
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"Gemini API configured. Model: {GEMINI_MODEL}")
else:
    print("Warning: GEMINI_API_KEY not found in environment variables")

app = FastAPI(title="Atlas API", version="0.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class WorkspaceCreateRequest(BaseModel):
    query: str


class WorkspaceType(BaseModel):
    workspace_type: str
    confidence: float
    rationale: str


class Module(BaseModel):
    type: str


class SourceQueries(BaseModel):
    maps: Optional[List[str]] = None
    reddit: Optional[List[str]] = None
    youtube: Optional[List[str]] = None
    web: Optional[List[str]] = None
    academic: Optional[List[str]] = None


class WorkspaceSchema(BaseModel):
    title: str
    modules: List[Module]
    recommended_sources: List[str]
    source_queries: SourceQueries


class Evidence(BaseModel):
    source: str
    label: str
    url: str


class Suggestion(BaseModel):
    title: str
    category: str
    reason: str
    evidence: List[Evidence]
    actions: List[str]


class SuggestionsResponse(BaseModel):
    suggestions: List[Suggestion]


# API Endpoints

@app.get("/")
def root():
    return {"message": "Atlas API is running"}


@app.get("/api/models")
def list_models():
    """List available Gemini models"""
    try:
        if not GEMINI_API_KEY:
            return {"error": "Gemini API key not configured"}
        models = genai.list_models()
        available_models = []
        for model in models:
            if "generateContent" in model.supported_generation_methods:
                available_models.append({
                    "name": model.name,
                    "display_name": model.display_name,
                    "supported_generation_methods": model.supported_generation_methods
                })
        return {
            "models": available_models,
            "model_names": [m["name"] for m in available_models]
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


def get_available_models():
    """Get list of available model names"""
    try:
        if not GEMINI_API_KEY:
            return []
        models = genai.list_models()
        return [
            model.name.split("/")[-1]  # Extract just the model name part
            for model in models
            if "generateContent" in model.supported_generation_methods
        ]
    except Exception as e:
        print(f"Error listing models: {e}")
        return []


def call_gemini(prompt: str, system_instruction: str = "") -> str:
    """Helper function to call Gemini API"""
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API key not configured")
    
    # Get available models first
    available_models = get_available_models()
    print(f"Available models: {available_models}")
    
    # Map user-friendly names to actual API model names
    model_name_mapping = {
        "gemini-2.5-flash": "gemini-1.5-flash",  # Try flash if 2.5 doesn't exist
        "gemini-flash": "gemini-1.5-flash",
        "gemini-2.0-flash": "gemini-1.5-flash",
    }
    
    # Get the actual model name to try
    model_to_try = model_name_mapping.get(GEMINI_MODEL.lower(), GEMINI_MODEL)
    
    # Build list of models to try, prioritizing available ones
    model_names_to_try = []
    
    # First, try models that are actually available
    if available_models:
        # Try available models first
        for avail_model in available_models:
            if avail_model not in model_names_to_try:
                model_names_to_try.append(avail_model)
    
    # Then try common fallbacks
    fallback_models = [
        model_to_try,
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro",
        "gemini-1.0-pro",
    ]
    
    for fb_model in fallback_models:
        if fb_model not in model_names_to_try:
            model_names_to_try.append(fb_model)
    
    last_error = None
    for model_name in model_names_to_try:
        try:
            print(f"Trying Gemini model: {model_name}")
            model = genai.GenerativeModel(model_name)
            full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt
            print(f"\n=== PROMPT SENT TO AI ===")
            print(f"System Instruction:\n{system_instruction}\n")
            print(f"User Prompt:\n{prompt}\n")
            print(f"Full Prompt:\n{full_prompt}\n")
            print("=" * 50)
            response = model.generate_content(full_prompt)
            print(f"Successfully used model: {model_name}")
            return response.text
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            last_error = e
            continue
    
    # If all models failed, provide helpful error message
    error_msg = f"Error calling Gemini API: {str(last_error)}"
    if available_models:
        error_msg += f"\nAvailable models: {', '.join(available_models)}"
    else:
        error_msg += "\nNo models found. Check your API key and permissions."
    
    print(f"All model attempts failed. Last error: {last_error}")
    import traceback
    traceback.print_exc()
    raise HTTPException(status_code=500, detail=error_msg)


@app.post("/api/workspace/classify", response_model=WorkspaceType)
async def classify_query(request: WorkspaceCreateRequest):
    """
    Classify the user query into a workspace type using Gemini API.
    """
    # CUSTOMIZE THIS PROMPT: Edit the system_prompt to change how classification works
    system_prompt = """You are a query classifier for a research workspace application called Atlas. 
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

        Return ONLY valid JSON, no other text.
        Return JSON format: {"workspace_type": "...", "confidence": 0.0-1.0, "rationale": "..."}"""

    # CUSTOMIZE THIS PROMPT: Edit the user_prompt to change what context is sent with the query
    user_prompt = f"""Analyze this search query and classify it:
"{request.query}"

What type of research workspace does this query need?"""
    
    try:
        if GEMINI_API_KEY:
            response_text = call_gemini(user_prompt, system_prompt)
            # Extract JSON from response (handle markdown code blocks)
            response_text = response_text.strip()
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(response_text)
            return WorkspaceType(**result)
        else:
            # Fallback to rule-based classification
            query_lower = request.query.lower()
            if any(word in query_lower for word in ["trip", "travel", "visit", "vacation"]):
                return WorkspaceType(
                    workspace_type="travel_research",
                    confidence=0.85,
                    rationale="User is planning a trip or travel-related activity."
                )
            elif any(word in query_lower for word in ["buy", "purchase", "choose", "laptop", "product"]):
                return WorkspaceType(
                    workspace_type="purchase_research",
                    confidence=0.80,
                    rationale="User is researching a purchase decision."
                )
            elif any(word in query_lower for word in ["learn", "study", "plan", "course", "tutorial"]):
                return WorkspaceType(
                    workspace_type="learning_plan",
                    confidence=0.75,
                    rationale="User wants to create a learning or study plan."
                )
            else:
                return WorkspaceType(
                    workspace_type="project_planner",
                    confidence=0.70,
                    rationale="Default to project planner workspace type."
                )
    except Exception as e:
        print(f"Classification error: {e}")
        # Fallback to default
        return WorkspaceType(
            workspace_type="project_planner",
            confidence=0.50,
            rationale=f"Error in classification: {str(e)}"
        )


@app.post("/api/workspace/schema", response_model=WorkspaceSchema)
async def generate_schema(request: WorkspaceCreateRequest, workspace_type: str):
    """
    Generate workspace schema based on query and workspace type using Gemini API.
    """
    # CUSTOMIZE THIS PROMPT: Edit the system_prompt to change how schema generation works
    system_prompt = """You are a workspace schema generator for Atlas, a research workspace application.
Generate a workspace layout that helps users research their query effectively.

Return ONLY valid JSON, no other text.
Return JSON format:
{
  "title": "Descriptive Workspace Title (e.g., 'Japan Travel Planning Workspace')",
  "modules": [{"type": "sources_panel"}, {"type": "saved_panel"}, {"type": "suggestions_panel"}, ...],
  "recommended_sources": ["web", "reddit", "youtube", "maps", "academic"],
  "source_queries": {
    "maps": ["specific search queries for maps"],
    "reddit": ["specific search queries for Reddit"],
    "youtube": ["specific search queries for YouTube"],
    "web": ["specific search queries for web search"],
    "academic": ["specific search queries for academic sources"]
  }
}

Available module types:
- sources_panel: Always include
- saved_panel: Always include  
- suggestions_panel: Always include
- map_panel: For travel queries (destinations, locations)
- itinerary_panel: For travel queries (trip planning)
- budget_panel: For travel or purchase queries (cost planning)
- comparison_panel: For purchase queries (product comparison)
- spec_panel: For purchase queries (product specifications)
- schedule_panel: For learning plans (study schedules)
- curriculum_panel: For learning plans (course structure)

Choose modules that match the workspace type and query needs."""

    # CUSTOMIZE THIS PROMPT: Edit the user_prompt to add more context or instructions
    user_prompt = f"""User Query: "{request.query}"
Workspace Type: {workspace_type}

Generate a workspace schema with:
1. A descriptive title that reflects the query
2. Appropriate modules for this workspace type
3. Recommended sources (web, reddit, youtube, maps, academic) that would be useful
4. Specific search queries for each source type that would help research this query

Example for travel_research:
- maps: ["japan tourist attractions", "tokyo hotels"]
- web: ["japan travel guide", "best time to visit japan"]
- reddit: ["japan travel tips", "japan itinerary"]
- youtube: ["japan travel vlog", "tokyo travel guide"]"""

    try:
        if GEMINI_API_KEY:
            response_text = call_gemini(user_prompt, system_prompt)
            # Extract JSON from response
            response_text = response_text.strip()
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(response_text)
            # Convert modules dict to Module objects
            modules = [Module(type=m["type"]) for m in result.get("modules", [])]
            return WorkspaceSchema(
                title=result.get("title", f"{workspace_type.replace('_', ' ').title()} Workspace"),
                modules=modules,
                recommended_sources=result.get("recommended_sources", ["web"]),
                source_queries=SourceQueries(**result.get("source_queries", {}))
            )
        else:
            # Fallback implementation
            modules = [
                Module(type="sources_panel"),
                Module(type="saved_panel"),
                Module(type="suggestions_panel"),
            ]
            
            if workspace_type == "travel_research":
                modules.extend([
                    Module(type="map_panel"),
                    Module(type="itinerary_panel"),
                    Module(type="budget_panel"),
                ])
                recommended_sources = ["maps", "web", "reddit", "youtube"]
            elif workspace_type == "purchase_research":
                modules.extend([
                    Module(type="comparison_panel"),
                    Module(type="spec_panel"),
                ])
                recommended_sources = ["web", "reddit", "youtube"]
            elif workspace_type == "learning_plan":
                modules.extend([
                    Module(type="schedule_panel"),
                    Module(type="curriculum_panel"),
                ])
                recommended_sources = ["web", "youtube", "academic"]
            else:
                recommended_sources = ["web", "reddit"]
            
            return WorkspaceSchema(
                title=f"{workspace_type.replace('_', ' ').title()} Workspace",
                modules=modules,
                recommended_sources=recommended_sources,
                source_queries=SourceQueries()
            )
    except Exception as e:
        print(f"Schema generation error: {e}")
        # Fallback to default
        modules = [
            Module(type="sources_panel"),
            Module(type="saved_panel"),
            Module(type="suggestions_panel"),
        ]
        return WorkspaceSchema(
            title=f"{workspace_type.replace('_', ' ').title()} Workspace",
            modules=modules,
            recommended_sources=["web"],
            source_queries=SourceQueries()
        )


@app.post("/api/workspace/suggestions", response_model=SuggestionsResponse)
async def generate_suggestions(request: WorkspaceCreateRequest, workspace_type: str):
    """
    Generate evidence-linked suggestions using Gemini API.
    """
    # CUSTOMIZE THIS PROMPT: Edit the system_prompt to change how suggestions are generated
    system_prompt = """You are a research assistant for Atlas, a search engine that generates research workspaces.
Your job is to suggest relevant, high-quality resources that help users research their query - similar to what Google Search would return.

Generate 4-6 suggestions that are:
- Highly relevant to the user's query
- From reputable, well-known sources (like travel guides, review sites, official resources)
- Similar to top Google Search results for the query
- Actionable and useful for research

Return ONLY valid JSON, no other text.
Return JSON format:
{
  "suggestions": [
    {
      "title": "Descriptive title of the resource (e.g., 'Japan Travel Guide - Lonely Planet')",
      "category": "category (e.g., 'travel_guide', 'review_site', 'official_resource', 'community_forum')",
      "reason": "Brief explanation of why this resource is useful for the query",
      "evidence": [
        {"source": "web", "label": "Descriptive label (e.g., 'Lonely Planet Japan Guide')", "url": "https://example.com"},
        {"source": "reddit", "label": "Descriptive label (e.g., 'r/JapanTravel - Trip Planning Thread')", "url": "https://reddit.com/..."}
      ],
      "actions": ["save", "open"]
    }
  ]
}

Guidelines:
- For travel queries: Suggest travel guides (Lonely Planet, TripAdvisor, official tourism sites), booking sites, travel blogs, Reddit communities
- For purchase queries: Suggest review sites (Wirecutter, Consumer Reports), comparison sites, official product pages, user forums
- For learning queries: Suggest educational platforms (Coursera, freeCodeCamp), official documentation, tutorial sites, learning communities
- Use realistic, well-known website names and URLs
- Make evidence sources diverse (mix of web, reddit, youtube when appropriate)
- Do NOT suggest workplace/office tools unless the query is explicitly about work/projects
- Focus on resources that would appear in top Google Search results"""

    # CUSTOMIZE THIS PROMPT: Edit the user_prompt to add more context, examples, or instructions
    user_prompt = f"""User Query: "{request.query}"
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

Make suggestions specific, relevant, and from well-known sources. Include evidence links that represent the types of resources users would actually find."""

    try:
        if GEMINI_API_KEY:
            response_text = call_gemini(user_prompt, system_prompt)
            # Extract JSON from response
            response_text = response_text.strip()
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(response_text)
            suggestions = []
            for s in result.get("suggestions", []):
                evidence_list = [Evidence(**e) for e in s.get("evidence", [])]
                suggestions.append(Suggestion(
                    title=s.get("title", "Untitled"),
                    category=s.get("category", "general"),
                    reason=s.get("reason", ""),
                    evidence=evidence_list,
                    actions=s.get("actions", ["save", "open"])
                ))
            return SuggestionsResponse(suggestions=suggestions)
        else:
            # Fallback implementation
            return SuggestionsResponse(
                suggestions=[
                    Suggestion(
                        title="Sample Suggestion",
                        category="general",
                        reason="This is a placeholder suggestion with evidence links.",
                        evidence=[
                            Evidence(
                                source="web",
                                label="Example Source",
                                url="https://example.com"
                            )
                        ],
                        actions=["save", "open"]
                    )
                ]
            )
    except Exception as e:
        print(f"Suggestions generation error: {e}")
        # Fallback to default
        return SuggestionsResponse(
            suggestions=[
                Suggestion(
                    title="Sample Suggestion",
                    category="general",
                    reason="Error generating suggestions. Please try again.",
                    evidence=[],
                    actions=["save", "open"]
                )
            ]
        )


@app.post("/api/workspace/create")
async def create_workspace(request: WorkspaceCreateRequest):
    """
    Main endpoint: creates a workspace by classifying query and generating schema.
    """
    try:
        print(f"Creating workspace for query: {request.query}")
        
        # Classify query
        print("Classifying query...")
        classification = await classify_query(request)
        print(f"Classification result: {classification.workspace_type}")
        
        # Generate schema
        print("Generating schema...")
        schema = await generate_schema(request, classification.workspace_type)
        print(f"Schema generated: {schema.title}")
        
        # Generate suggestions
        print("Generating suggestions...")
        suggestions = await generate_suggestions(request, classification.workspace_type)
        print(f"Generated {len(suggestions.suggestions)} suggestions")
        
        workspace_id = f"ws_{abs(hash(request.query)) % 10000}"
        print(f"Workspace created with ID: {workspace_id}")
        
        # Convert suggestions to dict format for JSON serialization (using model_dump for Pydantic v2)
        try:
            suggestions_list = [s.model_dump() for s in suggestions.suggestions]
        except AttributeError:
            # Fallback for older Pydantic versions
            suggestions_list = [s.dict() for s in suggestions.suggestions]
        
        # Convert schema to dict (using model_dump for Pydantic v2)
        try:
            schema_dict = schema.model_dump()
        except AttributeError:
            # Fallback for older Pydantic versions
            schema_dict = schema.dict()
        
        return {
            "id": workspace_id,
            "query": request.query,
            "workspace_type": classification.workspace_type,
            "schema": schema_dict,
            "suggestions": suggestions_list,  # Return array of dicts directly
            "enabled_sources": schema.recommended_sources,
            "saved_items": [],
        }
    except Exception as e:
        print(f"Error in create_workspace: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error creating workspace: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
