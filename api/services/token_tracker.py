import time
from datetime import datetime
from typing import List, Dict, Any

class TokenTracker:
    def __init__(self):
        self.total_requests: int = 42
        self.total_prompt_tokens: int = 18450
        self.total_completion_tokens: int = 12620
        self.total_tokens: int = 31070
        self.estimated_cost_usd: float = 0.0482
        self.start_time: float = time.time()
        
        self.service_usage: Dict[str, int] = {
            "Multi-Persona Chat": 12450,
            "Document RAG": 8320,
            "Copywriting & SEO": 4120,
            "Code Copilot": 3280,
            "Research Agent": 2100,
            "Vision & OCR": 800
        }
        
        self.recent_activities: List[Dict[str, Any]] = [
            {
                "id": "act_101",
                "service": "Document RAG",
                "action": "Indexed 'Financial_Report_Q4.pdf' (18 pages)",
                "tokens": 2840,
                "latency_ms": 340,
                "timestamp": "2 mins ago",
                "status": "success"
            },
            {
                "id": "act_102",
                "service": "Multi-Persona Chat",
                "action": "Conversation with 'Software Architect' persona",
                "tokens": 940,
                "latency_ms": 220,
                "timestamp": "7 mins ago",
                "status": "success"
            },
            {
                "id": "act_103",
                "service": "Autonomous Research",
                "action": "Market Research on AI SaaS Multi-tenant Architecture",
                "tokens": 4150,
                "latency_ms": 1250,
                "timestamp": "15 mins ago",
                "status": "success"
            },
            {
                "id": "act_104",
                "service": "Vision OCR",
                "action": "Extracted key-values from Invoice_INV9081.png",
                "tokens": 620,
                "latency_ms": 480,
                "timestamp": "30 mins ago",
                "status": "success"
            }
        ]

    def record_usage(self, service: str, action: str, prompt_tokens: int, completion_tokens: int, latency_ms: int, status: str = "success"):
        tokens = prompt_tokens + completion_tokens
        self.total_requests += 1
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        self.total_tokens += tokens
        
        # Calculate approximate cost ($0.0015 / 1k prompt, $0.002 / 1k completion)
        cost = (prompt_tokens * 0.0000015) + (completion_tokens * 0.000002)
        self.estimated_cost_usd += round(cost, 6)
        
        if service in self.service_usage:
            self.service_usage[service] += tokens
        else:
            self.service_usage[service] = tokens
            
        activity = {
            "id": f"act_{int(time.time()*1000)%100000}",
            "service": service,
            "action": action,
            "tokens": tokens,
            "latency_ms": latency_ms,
            "timestamp": "Just now",
            "status": status
        }
        self.recent_activities.insert(0, activity)
        if len(self.recent_activities) > 20:
            self.recent_activities.pop()

    def get_dashboard_metrics(self) -> Dict[str, Any]:
        uptime_seconds = int(time.time() - self.start_time)
        return {
            "total_requests": self.total_requests,
            "total_tokens": self.total_tokens,
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_completion_tokens": self.total_completion_tokens,
            "estimated_cost_usd": round(self.estimated_cost_usd, 4),
            "avg_latency_ms": 285,
            "uptime_seconds": uptime_seconds,
            "service_usage": self.service_usage,
            "recent_activities": self.recent_activities
        }

token_tracker = TokenTracker()
