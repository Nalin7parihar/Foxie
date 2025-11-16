"""
ReAct Agent using LangGraph for autonomous code generation with self-correction.
Implements Reason -> Act -> Observe loop as a state graph.
"""
from typing import List, Dict, Any, Optional, Literal, Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from google import genai
from google.genai import types
import operator
import os
from dotenv import load_dotenv
from app.utils.api_key_manager import APIKeyManager

load_dotenv()


# ============================================================================
# LangGraph State Definition
# ============================================================================

class AgentState(TypedDict):
    """State managed by the LangGraph workflow."""
    # Input configuration
    project_name: str
    resource_name: str
    fields: List[Dict[str, str]]  # [{name, type}]
    max_steps: int
    
    # File planning and tracking
    planned_files: List[str]
    generated_files: Annotated[List[Dict[str, Any]], operator.add]  # Append-only
    validated_files: Annotated[List[str], operator.add]  # Append-only
    
    # Current iteration state
    current_step: int
    current_file: Optional[str]
    last_validation_errors: List[str]
    
    # Agent reasoning history
    messages: Annotated[List[Any], operator.add]  # LLM conversation
    thoughts: Annotated[List[str], operator.add]  # Reasoning steps
    actions: Annotated[List[str], operator.add]  # Actions taken
    observations: Annotated[List[str], operator.add]  # Results observed
    
    # Control flow
    is_complete: bool
    next_action: str  # "plan" | "generate" | "validate" | "fix" | "complete"


# ============================================================================
# Pydantic Models for Structured Output
# ============================================================================

class ThoughtStep(BaseModel):
    """Agent's reasoning about what to do next."""
    reasoning: str = Field(description="The agent's thought process")
    next_action: Literal["plan", "generate", "validate", "fix", "complete"] = Field(
        description="What the agent plans to do"
    )
    target_file: Optional[str] = Field(default=None, description="File to work on")


class FileGeneration(BaseModel):
    """Generated file content."""
    file_path: str
    content: str
    description: str


class ValidationResult(BaseModel):
    """Result of code validation."""
    success: bool
    message: str
    errors: List[str] = Field(default_factory=list)


# ============================================================================
# ReAct Agent with LangGraph
# ============================================================================


class ReActAgent:
    """
    Autonomous agent that uses LangGraph's StateGraph to implement ReAct loop.
    
    Graph Structure:
    START -> plan_files -> reason -> [generate | validate | fix | complete]
          -> reason -> ... (loop) -> END
    
    Process:
    1. PLAN: Determine which files need to be generated
    2. REASON: Think about what to do next
    3. ACT: Generate, validate, or fix a file
    4. OBSERVE: Check results and update state
    5. REPEAT until complete
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the ReAct agent with LangGraph workflow.
        
        Args:
            api_key: Google Gemini API key. If not provided, will try to load from:
                     1. GOOGLE_API_KEY environment variable
                     2. .env file
                     3. ~/.foxie/.env file
                     
        Raises:
            ValueError: If no API key is found in any location
        """
        # Get API key using priority system
        resolved_key = APIKeyManager.get_api_key(
            provided_key=api_key,
            raise_if_missing=True
        )
        
        self.client = genai.Client(api_key=resolved_key)
        # Use gemini-1.5-flash for better free tier limits
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.graph = self._build_graph()
        
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("plan_files", self._plan_files_node)
        workflow.add_node("reason", self._reason_node)
        workflow.add_node("generate", self._generate_node)
        workflow.add_node("validate", self._validate_node)
        workflow.add_node("fix", self._fix_node)
        
        # Define edges
        workflow.set_entry_point("plan_files")
        workflow.add_edge("plan_files", "reason")
        
        # Conditional routing from reason node
        workflow.add_conditional_edges(
            "reason",
            self._route_action,
            {
                "generate": "generate",
                "validate": "validate",
                "fix": "fix",
                "complete": END,
                "reason": "reason"  # Loop back
            }
        )
        
        # After action nodes, go back to reasoning
        workflow.add_edge("generate", "reason")
        workflow.add_edge("validate", "reason")
        workflow.add_edge("fix", "reason")
        
        return workflow.compile()
    
    def _route_action(self, state: AgentState) -> str:
        """Decide which node to go to next based on state."""
        if state["is_complete"] or state["current_step"] >= state["max_steps"]:
            return "complete"
        
        next_action = state.get("next_action", "reason")
        
        # Map actions to graph nodes
        action_map = {
            "generate": "generate",
            "validate": "validate",
            "fix": "fix",
            "complete": "complete",
            "plan": "reason"  # Planning is done, go to reason
        }
        
        return action_map.get(next_action, "reason")
        
    # ========================================================================
    # LangGraph Node Functions
    # ========================================================================
    
    def _plan_files_node(self, state: AgentState) -> Dict[str, Any]:
        """Node: Plan which files to generate."""
        print("📋 Planning file structure...")
        
        fields_str = ", ".join([f"{f['name']}:{f['type']}" for f in state["fields"]])
        
        prompt = f"""You are a senior FastAPI developer planning a CRUD feature implementation.

Project: {state["project_name"]}
Resource: {state["resource_name"]}
Fields: {fields_str}

List ALL the files that need to be generated for a complete FastAPI CRUD feature.
Return ONLY a Python list of file paths, nothing else.

Example output:
["app/core/config.py", "app/database/db_session.py", "app/models/base_model.py", "app/models/product.py", "app/schemas/product.py", "app/crud/product.py", "app/api/endpoints/product.py", "app/api/router.py", "app/dependencies/auth_dependency.py", "app/main.py"]
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        
        # Parse the response
        content = response.text.strip()
        if "```" in content:
            content = content.split("```")[1].replace("python", "").strip()
        
        try:
            planned_files = eval(content)
            print(f"   📝 Planned {len(planned_files)} files")
        except:
            # Fallback to default structure
            resource = state["resource_name"]
            planned_files = [
                "app/core/config.py",
                "app/database/db_session.py",
                "app/models/base_model.py",
                f"app/models/{resource}.py",
                f"app/schemas/{resource}.py",
                f"app/crud/{resource}.py",
                f"app/api/endpoints/{resource}.py",
                "app/api/router.py",
                "app/dependencies/auth_dependency.py",
                "app/main.py"
            ]
            print(f"   📝 Using default plan: {len(planned_files)} files")
        
        return {
            "planned_files": planned_files,
            "messages": [prompt, content],
            "next_action": "generate"
        }
    
    def _reason_node(self, state: AgentState) -> Dict[str, Any]:
        """Node: Agent thinks about what to do next."""
        step = state.get("current_step", 0)
        print(f"\n{'='*60}")
        print(f"🤔 Step {step + 1}: Reasoning...")
        print(f"{'='*60}")
        
        # Build context
        generated_files_str = "\n".join([f"- {f['file_path']} ✅" for f in state.get("generated_files", [])])
        validated_files_str = "\n".join([f"- {f} ✓" for f in state.get("validated_files", [])])
        pending_files = [
            f for f in state.get("planned_files", []) 
            if f not in [gf['file_path'] for gf in state.get("generated_files", [])]
        ]
        pending_files_str = "\n".join([f"- {f} ⏳" for f in pending_files])
        
        recent_thoughts = "\n".join(state.get("thoughts", [])[-3:]) if state.get("thoughts") else "None"
        recent_actions = "\n".join(state.get("actions", [])[-3:]) if state.get("actions") else "None"
        recent_observations = "\n".join(state.get("observations", [])[-3:]) if state.get("observations") else "None"
        
        fields_str = ", ".join([f"{f['name']}:{f['type']}" for f in state["fields"]])
        
        prompt = f"""You are an autonomous senior FastAPI developer using the ReAct (Reason + Act) pattern.

PROJECT CONTEXT:
- Project: {state['project_name']}
- Resource: {state['resource_name']}
- Fields: {fields_str}

CURRENT STATE:
Generated Files:
{generated_files_str if generated_files_str else "None yet"}

Validated Files:
{validated_files_str if validated_files_str else "None yet"}

Pending Files:
{pending_files_str if pending_files_str else "All done!"}

RECENT HISTORY:
Recent Thoughts:
{recent_thoughts}

Recent Actions:
{recent_actions}

Recent Observations:
{recent_observations}

YOUR TASK (ReAct Loop):
1. REASON: Think about what to do next
   - If there are pending files, which is most fundamental? (dependencies first!)
   - If a file was just generated, should it be validated?
   - If validation found errors, how to fix them?
   - If all files are generated and validated, mark as complete

2. Decide your next action:
   - "generate": Create the next most important file
   - "validate": Check a recently generated file
   - "fix": Fix errors found during validation
   - "complete": All files generated and validated

3. Explain your reasoning clearly

Return a JSON object with: {{"reasoning": "...", "next_action": "...", "target_file": "..."}}
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ThoughtStep,
                temperature=0.3
            )
        )
        
        thought = response.parsed
        print(f"   💭 Thought: {thought.reasoning[:100]}...")
        print(f"   🎯 Next Action: {thought.next_action}")
        if thought.target_file:
            print(f"   📄 Target: {thought.target_file}")
        
        # Enforce max_steps limit strictly
        next_step = step + 1
        if next_step >= state.get("max_steps", 50):
            print(f"   ⚠️  Max steps ({state.get('max_steps', 50)}) reached. Completing...")
            thought.next_action = "complete"
        
        # Check completion conditions
        is_complete = (
            thought.next_action == "complete" or
            (len(state.get("validated_files", [])) == len(state.get("planned_files", [])) and
             len(state.get("validated_files", [])) > 0) or
            next_step >= state.get("max_steps", 50)
        )
        
        return {
            "current_step": step + 1,
            "current_file": thought.target_file,
            "next_action": thought.next_action,
            "is_complete": is_complete,
            "thoughts": [thought.reasoning],
            "messages": state.get("messages", []) + [prompt, response.text]
        }
    
    def _generate_node(self, state: AgentState) -> Dict[str, Any]:
        """Node: Generate a file."""
        # Determine which file to generate
        target_file = state.get("current_file")
        if not target_file:
            # Pick first pending file
            pending = [
                f for f in state.get("planned_files", []) 
                if f not in [gf['file_path'] for gf in state.get("generated_files", [])]
            ]
            if not pending:
                return {"next_action": "complete", "is_complete": True}
            target_file = pending[0]
        
        print(f"   ✍️  Generating: {target_file}")
        
        from app.core.file_generator import FileGenerator
        generator = FileGenerator()
        
        # Collect context
        context = {gf['file_path']: gf['content'] for gf in state.get("generated_files", [])}
        
        try:
            content = generator.generate_file(
                file_path=target_file,
                project_name=state["project_name"],
                resource_name=state["resource_name"],
                fields=state["fields"],
                context=context
            )
            
            # Clean markdown if present
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1]) if len(lines) > 2 else content
            
            generated_file = {
                'file_path': target_file,
                'content': content,
                'description': f"Generated {target_file}",
                'status': 'generated'
            }
            
            # Auto-validate
            print(f"   🔍 Auto-validating {target_file}...")
            validation_result = self._validate_code(target_file, content)
            
            if validation_result.success:
                generated_file['status'] = 'validated'
                print(f"   ✅ {target_file} passed validation!")
                return {
                    "generated_files": [generated_file],
                    "validated_files": [target_file],
                    "actions": [f"Generated and validated {target_file}"],
                    "observations": [validation_result.message],
                    "next_action": "generate"  # Continue to next file
                }
            else:
                print(f"   ⚠️  Validation errors: {', '.join(validation_result.errors[:2])}")
                return {
                    "generated_files": [generated_file],
                    "actions": [f"Generated {target_file} (has errors)"],
                    "observations": [validation_result.message],
                    "last_validation_errors": validation_result.errors,
                    "next_action": "fix"  # Need to fix
                }
                
        except Exception as e:
            print(f"   ❌ Generation failed: {e}")
            return {
                "actions": [f"Failed to generate {target_file}: {str(e)}"],
                "observations": [f"Error: {str(e)}"],
                "next_action": "generate"  # Try next file
            }
    
    def _validate_node(self, state: AgentState) -> Dict[str, Any]:
        """Node: Validate a file."""
        target_file = state.get("current_file")
        if not target_file:
            return {"next_action": "reason"}
        
        print(f"   🔍 Validating: {target_file}")
        
        # Find file content
        file_content = None
        for gf in state.get("generated_files", []):
            if gf['file_path'] == target_file:
                file_content = gf['content']
                break
        
        if not file_content:
            print(f"   ⚠️  File {target_file} not found")
            return {
                "observations": [f"File {target_file} not generated yet"],
                "next_action": "generate"
            }
        
        validation_result = self._validate_code(target_file, file_content)
        
        if validation_result.success:
            print(f"   ✅ Validation passed!")
            return {
                "validated_files": [target_file],
                "observations": [validation_result.message],
                "next_action": "generate"  # Continue to next file
            }
        else:
            print(f"   ❌ Validation failed: {len(validation_result.errors)} issues")
            for error in validation_result.errors[:3]:
                print(f"      • {error}")
            return {
                "observations": [validation_result.message],
                "last_validation_errors": validation_result.errors,
                "next_action": "fix"
            }
    
    def _fix_node(self, state: AgentState) -> Dict[str, Any]:
        """Node: Fix a file that has errors."""
        target_file = state.get("current_file")
        if not target_file:
            return {"next_action": "reason"}
        
        print(f"   🔧 Fixing: {target_file}")
        
        # This will re-generate the file
        # Remove from generated_files to trigger fresh generation
        updated_files = [
            gf for gf in state.get("generated_files", [])
            if gf['file_path'] != target_file
        ]
        
        # Note: We're effectively delegating to generate node
        # by removing the file and setting next_action to generate
        return {
            "generated_files": updated_files,
            "actions": [f"Fixing {target_file} by regenerating"],
            "next_action": "generate"
        }
    
    def _validate_code(self, file_path: str, content: str) -> ValidationResult:
        """Helper: Validate code using validators."""
        from app.utils.validators import CodeValidator
        
        results = CodeValidator.validate_all(content, file_path)
        
        if not results:
            return ValidationResult(
                success=True,
                message=f"✅ {file_path} passed all validations",
                errors=[]
            )
        
        errors = []
        for result in results:
            errors.extend(result.issues)
        
        return ValidationResult(
            success=False,
            message=f"❌ {file_path} has {len(errors)} issue(s)",
            errors=errors
        )
    
    # ========================================================================
    # Run Method - Uses LangGraph
    # ========================================================================
    
    def run(self, 
            project_name: str, 
            resource_name: str, 
            fields: List[Dict[str, str]],
            max_steps: int = 50) -> Dict[str, Any]:
        """
        Run the ReAct agent using LangGraph.
        
        Returns:
            Dictionary with generated files and execution summary
        """
        print(f"\n🦊 Starting LangGraph ReAct Agent for '{resource_name}' resource...")
        print(f"   Project: {project_name}")
        fields_str = ', '.join([f"{f['name']}:{f['type']}" for f in fields])
        print(f"   Fields: {fields_str}")
        
        # Initialize state
        initial_state: AgentState = {
            "project_name": project_name,
            "resource_name": resource_name,
            "fields": fields,
            "max_steps": max_steps,
            "current_step": 0,
            "planned_files": [],
            "generated_files": [],
            "validated_files": [],
            "messages": [],
            "thoughts": [],
            "actions": [],
            "observations": [],
            "current_file": None,
            "next_action": "plan",
            "is_complete": False,
            "last_validation_errors": []
        }
        
        # Run the graph
        # Set recursion_limit higher than max_steps to allow completion
        # Each step might trigger multiple graph nodes (reason -> generate -> reason)
        recursion_limit = max(max_steps + 10, 30)  # At least 30, or max_steps + 10
        print(f"\n🔄 Executing LangGraph workflow (max_steps: {max_steps}, recursion_limit: {recursion_limit})...")
        final_state = self.graph.invoke(
            initial_state,
            config={"recursion_limit": recursion_limit}
        )
        
        # Final summary
        print(f"\n{'='*60}")
        print(f"🏁 LangGraph ReAct Agent Completed")
        print(f"{'='*60}")
        print(f"   Total Steps: {final_state.get('current_step', 0)}")
        print(f"   Files Generated: {len(final_state.get('generated_files', []))}")
        print(f"   Files Validated: {len(final_state.get('validated_files', []))}")
        print(f"   Completion Status: {'✅ Success' if final_state.get('is_complete', False) else '⚠️  Incomplete'}")
        
        return {
            "generated_files": final_state.get("generated_files", []),
            "validated_files": final_state.get("validated_files", []),
            "total_steps": final_state.get("current_step", 0),
            "thought_history": final_state.get("thoughts", []),
            "action_history": final_state.get("actions", []),
            "observation_history": final_state.get("observations", []),
            "is_complete": final_state.get("is_complete", False),
            "planned_files": final_state.get("planned_files", [])
        }
