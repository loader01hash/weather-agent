"""Message structures for agent communication."""

from typing import Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum


class MessageType(Enum):
    """Types of messages agents can exchange."""
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    ERROR = "error"
    INFO = "info"


class TaskType(Enum):
    """Types of tasks Agent B can perform."""
    GET_WEATHER = "get_weather"
    SUMMARIZE = "summarize"
    CALCULATE = "calculate"
    
    # New insight generation task types
    GENERATE_WEATHER_INSIGHTS = "generate_weather_insights"
    ANALYZE_COMFORT_CONDITIONS = "analyze_comfort_conditions"
    SUGGEST_ACTIVITIES = "suggest_activities"
    ASSESS_HEALTH_FACTORS = "assess_health_factors"


@dataclass
class Message:
    """Base message structure for agent communication."""
    type: MessageType
    sender: str
    receiver: str
    content: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "type": self.type.value,
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "metadata": self.metadata
        }


@dataclass
class Task:
    """Represents a task to be executed."""
    task_type: TaskType
    parameters: Dict[str, Any]
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "task_type": self.task_type.value,
            "parameters": self.parameters,
            "description": self.description
        }


@dataclass
class TaskResult:
    """Result of a task execution."""
    success: bool
    data: Any
    error: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error
        }


@dataclass
class InsightResult:
    """Result of insight generation with categorized recommendations."""
    category: str  # "comfort", "activities", "health", "clothing", "safety"
    insights: List[str]
    recommendations: List[str]
    priority: int = 1  # 1-5, higher is more important
    confidence: float = 1.0  # 0.0-1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert insight result to dictionary."""
        return {
            "category": self.category,
            "insights": self.insights,
            "recommendations": self.recommendations,
            "priority": self.priority,
            "confidence": self.confidence
        }