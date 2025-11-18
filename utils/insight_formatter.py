"""Insight formatting and presentation utilities."""

from typing import Dict, Any, List
from utils.message import InsightResult


class InsightFormatter:
    """
    Formats and categorizes weather insights for presentation.
    Handles prioritization and relevance filtering.
    """
    
    def __init__(self):
        """Initialize the insight formatter."""
        self.category_priorities = {
            "health": 5,      # Highest priority - safety first
            "comfort": 4,     # High priority - immediate impact
            "activities": 3,  # Medium priority - planning
            "clothing": 2,    # Lower priority - practical
            "patterns": 1     # Lowest priority - informational
        }
        
        self.category_display_names = {
            "comfort": "Comfort Level",
            "activities": "Activity Suggestions", 
            "health": "Health & Safety",
            "clothing": "Clothing Recommendations",
            "patterns": "Weather Patterns"
        }
    
    def prioritize_insights(self, insights_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Prioritize insights based on category importance and insight priority.
        
        Args:
            insights_data: Dictionary containing insight results by category
            
        Returns:
            List of prioritized insights sorted by importance
        """
        prioritized = []
        
        for category, insight_data in insights_data.items():
            if isinstance(insight_data, dict) and insight_data.get("recommendations"):
                category_priority = self.category_priorities.get(category, 1)
                insight_priority = insight_data.get("priority", 1)
                
                # Combined priority score (category weight * insight priority)
                combined_priority = category_priority * insight_priority
                
                prioritized.append({
                    "category": category,
                    "display_name": self.category_display_names.get(category, category.capitalize()),
                    "data": insight_data,
                    "priority_score": combined_priority
                })
        
        # Sort by priority score (highest first)
        return sorted(prioritized, key=lambda x: x["priority_score"], reverse=True)
    
    def filter_relevant_insights(self, insights: List[Dict[str, Any]], max_insights: int = 3) -> List[Dict[str, Any]]:
        """
        Filter insights to show only the most relevant ones.
        
        Args:
            insights: List of prioritized insights
            max_insights: Maximum number of insights to return
            
        Returns:
            Filtered list of most relevant insights
        """
        # Filter out low-priority insights if we have too many
        if len(insights) <= max_insights:
            return insights
        
        # Keep high-priority insights (priority score >= 8) and fill remaining slots
        high_priority = [i for i in insights if i["priority_score"] >= 8]
        remaining_slots = max_insights - len(high_priority)
        
        if remaining_slots > 0:
            other_insights = [i for i in insights if i["priority_score"] < 8]
            high_priority.extend(other_insights[:remaining_slots])
        
        return high_priority[:max_insights]
    
    def format_insight_category(self, insight: Dict[str, Any], include_title: bool = True) -> str:
        """
        Format a single insight category for display.
        
        Args:
            insight: Insight data with category and recommendations
            include_title: Whether to include category title
            
        Returns:
            Formatted string for the insight category
        """
        data = insight["data"]
        recommendations = data.get("recommendations", [])
        
        if not recommendations:
            return ""
        
        formatted_parts = []
        
        if include_title:
            formatted_parts.append(f"**{insight['display_name']}:**")
        
        # Limit recommendations based on priority
        priority = data.get("priority", 1)
        max_recommendations = min(4 if priority >= 4 else 3, len(recommendations))
        
        for i, rec in enumerate(recommendations[:max_recommendations]):
            formatted_parts.append(f"• {rec}")
        
        return "\n".join(formatted_parts)
    
    def format_comprehensive_insights(self, insights_data: Dict[str, Any]) -> str:
        """
        Format comprehensive insights for display.
        
        Args:
            insights_data: Complete insights data from multiple categories
            
        Returns:
            Formatted string with all relevant insights
        """
        prioritized = self.prioritize_insights(insights_data)
        relevant = self.filter_relevant_insights(prioritized, max_insights=4)
        
        if not relevant:
            return ""
        
        formatted_sections = []
        
        for insight in relevant:
            section = self.format_insight_category(insight, include_title=True)
            if section:
                formatted_sections.append(section)
        
        return "\n\n".join(formatted_sections)
    
    def create_summary_insights(self, insights_data: Dict[str, Any]) -> str:
        """
        Create a brief summary of the most important insights.
        
        Args:
            insights_data: Complete insights data from multiple categories
            
        Returns:
            Brief summary string with key insights
        """
        prioritized = self.prioritize_insights(insights_data)
        
        if not prioritized:
            return ""
        
        # Get the top insight from each high-priority category
        summary_parts = []
        seen_categories = set()
        
        for insight in prioritized:
            if len(summary_parts) >= 3:  # Limit summary to 3 key points
                break
                
            category = insight["category"]
            if category in seen_categories:
                continue
                
            data = insight["data"]
            recommendations = data.get("recommendations", [])
            
            if recommendations and insight["priority_score"] >= 6:
                summary_parts.append(recommendations[0])  # Take the first (most important) recommendation
                seen_categories.add(category)
        
        return " ".join(summary_parts) if summary_parts else ""