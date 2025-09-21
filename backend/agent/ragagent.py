from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import List, Dict, Any, TypedDict, Annotated, Optional
from datetime import datetime
import json
from langgraph.graph import StateGraph, END
from langchain_core.documents import Document
from dotenv import load_dotenv
import requests
from duckduckgo_search import DDGS

# Load environment variables
load_dotenv()

# Initialize OpenAI client
from openai import OpenAI

# Global client instance
client = None

def get_openai_client():
    """Get or create OpenAI client instance"""
    global client
    if client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        try:
            client = OpenAI(api_key=api_key)
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}")
            client = None
    
    return client

# Pydantic models for API
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime

class AgentState(TypedDict):
    messages: Annotated[List[Any], "The messages in the conversation"]
    query: str
    context: str
    web_search_results: List[Dict]
    rag_results: List[Document]
    final_answer: str
    next_action: str

class UAFKnowledgeBase:
    """Knowledge base for UAF University information"""
    
    def __init__(self):
        self.json_docs = []
        self._load_json_data()

    def _load_json_data(self):
        """Load university data from uaf_scraped_data.json"""
        try:
            with open("uaf_data/uaf_scraped_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            self.json_docs = [
                Document(
                    page_content=entry.get("content", ""),
                    metadata=entry.get("metadata", {})
                )
                for entry in data
            ]
            print(f"Loaded {len(self.json_docs)} documents from uaf_scraped_data.json")
        except Exception as e:
            print(f"Could not load JSON data: {str(e)}")
            self.json_docs = []

    def retrieve_context(self, query: str) -> List[Document]:
        """Retrieve relevant context for query from knowledge base"""
        results = []
        
        if self.json_docs:
            keywords = query.lower().split()
            scored_docs = []
            
            for doc in self.json_docs:
                content = doc.page_content.lower()
                title = str(doc.metadata.get("title", "")).lower()
                
                # Calculate relevance score
                score = 0
                for keyword in keywords:
                    if keyword in content:
                        score += content.count(keyword)
                    if keyword in title:
                        score += title.count(keyword) * 2
                
                if score > 0:
                    scored_docs.append((doc, score))
            
            # Sort by score and return top 5
            scored_docs.sort(key=lambda x: x[1], reverse=True)
            results = [doc for doc, score in scored_docs[:5]]
        
        return results

class UAFWebSearchTool:
    """Web search tool using DuckDuckGo for UAF University information"""
     
    def __init__(self):
        self.ddgs = DDGS()

    def search_duckduckgo(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search using DuckDuckGo"""
        try:
            results = []
            search_results = self.ddgs.text(query, max_results=max_results)
            
            for result in search_results:
                results.append({
                    "title": result.get("title", ""),
                    "snippet": result.get("body", ""),
                    "url": result.get("href", ""),
                    "source": "DuckDuckGo"
                })
            
            return results
            
        except Exception as e:
            print(f"Error in DuckDuckGo search: {str(e)}")
            return []

    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for information using DuckDuckGo"""
        # Use DuckDuckGo for all searches
        results = self.search_duckduckgo(query, max_results)
        
        return results or [{
            "title": "Search Error",
            "snippet": "Could not perform web search",
            "url": "",
            "source": "Error"
        }]

class UAFAgentTool:
    """UAF University AI Agent Tool"""
    
    def __init__(self):
        self.knowledge_base = UAFKnowledgeBase()
        self.web_search = UAFWebSearchTool()
        self.graph = None
        self._build_graph()
        
    def _get_llm_response(self, messages: List[Dict]) -> str:
        """Get response from LLM"""
        try:
            client = get_openai_client()
            
            if client is None:
                return self._get_llm_response_fallback(messages)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM response error: {e}")
            return self._get_llm_response_fallback(messages)
    
    def _get_llm_response_fallback(self, messages: List[Dict]) -> str:
        """Fallback method using requests directly"""
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                return "Error: OPENAI_API_KEY not configured"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-4o-mini",
                "messages": messages,
                "temperature": 0.1
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Error: API request failed with status {response.status_code}"
                
        except Exception as e:
            return f"Error: {str(e)}"
        
    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("uaf_filter", self.uaf_filter)
        workflow.add_node("retrieve_knowledge", self.retrieve_knowledge)
        workflow.add_node("web_search", self.web_search_node)
        workflow.add_node("generate_response", self.generate_response)
        
        # Add edges
        workflow.set_entry_point("uaf_filter")
        workflow.add_edge("uaf_filter", "retrieve_knowledge")
        workflow.add_edge("retrieve_knowledge", "web_search")
        workflow.add_edge("web_search", "generate_response")
        workflow.add_edge("generate_response", END)
        
        self.graph = workflow.compile()
        
    def uaf_filter(self, state: AgentState) -> AgentState:
        """Filter to only answer UAF University-related queries"""
        query = state["query"].lower()
        uaf_keywords = [
            "uaf", "university of agriculture", "faisalabad",
            "agriculture university", "uaf.edu.pk", "agriculture faisalabad"
        ]
        
        is_uaf_related = any(keyword in query for keyword in uaf_keywords)
        
        if not is_uaf_related:
            state["final_answer"] = "I can only answer questions related to UAF (University of Agriculture, Faisalabad). Please ask something about UAF University."
            state["next_action"] = "end"
        else:
            state["next_action"] = "continue"
            
        return state
    
    def retrieve_knowledge(self, state: AgentState) -> AgentState:
        """Retrieve information from UAF knowledge base"""
        if state.get("next_action") == "end":
            return state
            
        query = state["query"]
        docs = self.knowledge_base.retrieve_context(query)
        state["rag_results"] = docs
        
        if docs:
            context = "\n".join([doc.page_content for doc in docs])
            state["context"] = context
        else:
            state["context"] = "No relevant information found in knowledge base."
            
        return state
    
    def web_search_node(self, state: AgentState) -> AgentState:
        """Search web for additional information"""
        if state.get("next_action") == "end":
            return state
            
        query = state["query"]
        results = self.web_search.search(query)
        state["web_search_results"] = results
        return state
    
    def generate_response(self, state: AgentState) -> AgentState:
        """Generate final response using LLM"""
        if state.get("next_action") == "end":
            return state
            
        query = state["query"]
        context = state.get("context", "")
        web_results = state.get("web_search_results", [])
        
        # Prepare web search context
        web_context = ""
        if web_results:
            web_context = "\n\nRecent web search results:\n"
            for result in web_results:
                web_context += f"- {result['title']}: {result['snippet']}\n"
        
        messages = [
            {
                "role": "system", 
                "content": """You are a helpful assistant specializing in UAF (University of Agriculture, Faisalabad) information. 
                Use the provided context to answer questions about UAF University accurately and comprehensively.
                If you don't have specific information, be honest about it.
                Focus only on UAF University-related information.
                Use markdown for formatting when appropriate."""
            },
            {
                "role": "user", 
                "content": f"""
                Question: {query}
                
                Knowledge Base Context:
                {context}
                
                {web_context}
                
                Please provide a comprehensive answer about UAF (University of Agriculture, Faisalabad) based on the available information.
                """
            }
        ]
        
        response = self._get_llm_response(messages)
        state["final_answer"] = response
            
        return state
    
    def generate_response_for_query(self, message: str) -> str:
        """Main method to generate response for a user message"""
        # Handle greetings
        if message.strip().lower() in ["hello", "hi", "salam", "assalamualaikum", "assalamu alaikum"]:
            return "Hi! I am UAF (University of Agriculture, Faisalabad) AI assistant. How can I help you with information about UAF University?"

        # Initialize state
        initial_state = AgentState(
            messages=[],
            query=message,
            context="",
            web_search_results=[],
            rag_results=[],
            final_answer="",
            next_action=""
        )
        
        try:
            # Run the agent workflow
            result = self.graph.invoke(initial_state)
            return result["final_answer"]
        except Exception as e:
            return f"Error processing your request: {str(e)}"

# FastAPI app initialization
app = FastAPI(
    title="UAF University AI Assistant",
    description="AI Assistant for UAF (University of Agriculture, Faisalabad)",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent tool instance
agent_tool = None

def get_agent_tool():
    """Get or create agent tool instance"""
    global agent_tool
    if agent_tool is None:
        try:
            agent_tool = UAFAgentTool()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error initializing agent tool: {str(e)}")
    return agent_tool

@app.on_event("startup")
async def startup_event():
    """Initialize the agent tool on startup"""
    try:
        aimlapi_key = os.getenv("AIMLAPI_KEY")
        if not aimlapi_key:
            print("Warning: AIMLAPI_KEY not found in environment variables")
            return
        
        # Initialize agent tool
        global agent_tool
        agent_tool = UAFAgentTool()
        print("UAF University AI Assistant started successfully")
    except Exception as e:
        print(f"Error during startup: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "UAF University AI Assistant",
        "description": "AI Assistant for UAF (University of Agriculture, Faisalabad)",
        "university": "University of Agriculture, Faisalabad",
        "established": "1906",
        "website": "https://uaf.edu.pk",
        "endpoints": {
            "GET /": "API information and UAF University details",
            "GET /health": "Health check endpoint", 
            "POST /chat": "Chat with UAF University AI Assistant"
        },
        "usage": {
            "chat_endpoint": "Send POST request to /chat with JSON: {\"message\": \"your question about UAF\"}"
        },
        "contact": {
            "address": "University of Agriculture, Faisalabad - 38040, Punjab, Pakistan",
            "phone": "+92-41-9200161",
            "email": "info@uaf.edu.pk"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "service": "UAF University AI Assistant",
        "api_key_configured": bool(os.getenv("AIMLAPI_KEY")),
        "serp_api_configured": bool(os.getenv("SERP_API_KEY")),
        "agent_tool_status": "initialized" if agent_tool else "not initialized"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """Chat endpoint that calls the agent tool to generate responses"""
    try:
        # Get the agent tool
        tool = get_agent_tool()
        
        # Generate response using the agent tool
        response = tool.generate_response_for_query(request.message)
        
        return ChatResponse(
            response=response,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)