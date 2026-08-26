import time
import json
import httpx
from typing import Dict, Any, List, Optional
from config import config

class AIEngine:
    """Unified multi-model AI engine supporting Groq, Gemini, OpenAI and Smart Demo Mode."""
    
    @staticmethod
    async def generate_response(
        system_prompt: str,
        user_message: str,
        history: Optional[List[Dict[str, str]]] = None,
        model: Optional[str] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        start_time = time.time()
        
        # Check if Demo Mode or No API Key configured
        if config.DEMO_MODE or config.ACTIVE_PROVIDER == "demo":
            return await AIEngine._smart_demo_chat(system_prompt, user_message)
            
        # Call Groq API if active
        if config.ACTIVE_PROVIDER == "groq" and config.GROQ_API_KEY:
            try:
                headers = {
                    "Authorization": f"Bearer {config.GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }
                messages = [{"role": "system", "content": system_prompt}]
                if history:
                    messages.extend(history)
                messages.append({"role": "user", "content": user_message})
                
                payload = {
                    "model": model or "llama-3.3-70b-versatile",
                    "messages": messages,
                    "temperature": temperature
                }
                async with httpx.AsyncClient(timeout=30.0) as client:
                    resp = await client.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        reply = data["choices"][0]["message"]["content"]
                        prompt_tok = data.get("usage", {}).get("prompt_tokens", 120)
                        comp_tok = data.get("usage", {}).get("completion_tokens", 250)
                        latency = int((time.time() - start_time) * 1000)
                        return {
                            "response": reply,
                            "prompt_tokens": prompt_tok,
                            "completion_tokens": comp_tok,
                            "latency_ms": latency,
                            "provider": "groq",
                            "model": model or "llama-3.3-70b-versatile"
                        }
            except Exception as e:
                # Fallback to demo mode gracefully
                pass
                
        # Call Gemini API if active
        if config.ACTIVE_PROVIDER == "gemini" and config.GEMINI_API_KEY:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={config.GEMINI_API_KEY}"
                payload = {
                    "contents": [{"parts": [{"text": f"{system_prompt}\n\nUser Question: {user_message}"}]}]
                }
                async with httpx.AsyncClient(timeout=30.0) as client:
                    resp = await client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        reply = data["candidates"][0]["content"]["parts"][0]["text"]
                        latency = int((time.time() - start_time) * 1000)
                        return {
                            "response": reply,
                            "prompt_tokens": len(user_message)//4 + 50,
                            "completion_tokens": len(reply)//4,
                            "latency_ms": latency,
                            "provider": "gemini",
                            "model": "gemini-1.5-flash"
                        }
            except Exception:
                pass

        # Call OpenAI API if active
        if config.ACTIVE_PROVIDER == "openai" and config.OPENAI_API_KEY:
            try:
                headers = {
                    "Authorization": f"Bearer {config.OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                }
                messages = [{"role": "system", "content": system_prompt}]
                if history:
                    messages.extend(history)
                messages.append({"role": "user", "content": user_message})
                payload = {
                    "model": model or "gpt-4o-mini",
                    "messages": messages,
                    "temperature": temperature
                }
                async with httpx.AsyncClient(timeout=30.0) as client:
                    resp = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        reply = data["choices"][0]["message"]["content"]
                        prompt_tok = data.get("usage", {}).get("prompt_tokens", 100)
                        comp_tok = data.get("usage", {}).get("completion_tokens", 200)
                        latency = int((time.time() - start_time) * 1000)
                        return {
                            "response": reply,
                            "prompt_tokens": prompt_tok,
                            "completion_tokens": comp_tok,
                            "latency_ms": latency,
                            "provider": "openai",
                            "model": model or "gpt-4o-mini"
                        }
            except Exception:
                pass

        # Fallback to Smart Demo Mode
        return await AIEngine._smart_demo_chat(system_prompt, user_message)

    @staticmethod
    async def _smart_demo_chat(system_prompt: str, user_message: str) -> Dict[str, Any]:
        """Provides realistic contextual simulated responses for smooth demo experience."""
        time.sleep(0.3)
        msg_lower = user_message.lower()
        
        if "architect" in system_prompt.lower():
            reply = (
                f"### 🏗️ Software Architecture Recommendation\n\n"
                f"Based on your query regarding: **{user_message}**\n\n"
                f"1. **Scalability & Decoupling:** Recommend an Event-Driven Architecture (EDA) with a high-throughput message broker like Apache Kafka or RabbitMQ.\n"
                f"2. **Database Tier:** Utilize PostgreSQL for ACID-compliant transactional data and Redis for fast in-memory session and cache storage.\n"
                f"3. **Security & API Gateway:** Enforce JWT token verification, Rate Limiting (Token Bucket algorithm), and CORS isolation at the NGINX or Envoy layer.\n"
                f"4. **Deployment:** Dockerized containers orchestrated via Kubernetes (EKS/GKE) with Horizontal Pod Autoscaling (HPA) enabled."
            )
        elif "business" in system_prompt.lower() or "consultant" in system_prompt.lower():
            reply = (
                f"### 💼 Business Strategy & Monetization Insight\n\n"
                f"Analyzing your topic: **{user_message}**\n\n"
                f"- **Value Proposition:** Focus on minimizing Customer Acquisition Cost (CAC) while scaling Lifetime Value (LTV) through multi-tiered SaaS subscriptions (Starter, Pro, Enterprise).\n"
                f"- **Go-To-Market (GTM):** Implement Product-Led Growth (PLG) with a generous free tier / trial to drive virality and quick onboarding.\n"
                f"- **Key Metrics:** Track Net Revenue Retention (NRR > 115%), Monthly Recurring Revenue (MRR), and Churn rate (< 2% monthly)."
            )
        elif "copywriter" in system_prompt.lower():
            reply = (
                f"### ✍️ High-Converting Copywriting Output\n\n"
                f"**Headline:** Unlock 10x Operational Speed with Intelligent AI SaaS Automation\n\n"
                f"**Hook:** Stop spending countless hours on repetitive manual workflows. Our all-in-one AI platform turns complex tasks into 1-click execution.\n\n"
                f"**Call to Action (CTA):** [Start Your Free 14-Day Trial Today — No Credit Card Required!]"
            )
        elif "legal" in system_prompt.lower():
            reply = (
                f"### ⚖️ Legal & Compliance Framework Assessment\n\n"
                f"Regarding: *{user_message}*\n\n"
                f"- **Data Privacy Compliance:** Ensure full adherence to GDPR (Articles 6 & 13) and CCPA regarding user consent, data retention, and Right to be Forgotten.\n"
                f"- **Terms of Service:** Mandate clear disclaimer of liability for generative AI outputs and state user ownership of uploaded data.\n"
                f"- **Data Processing Addendum (DPA):** Standardize standard contractual clauses (SCCs) for all third-party sub-processors."
            )
        else:
            reply = (
                f"Hello! I am your AI assistant. Regarding your request: **'{user_message}'**\n\n"
                f"Here are the key points to consider:\n"
                f"- ✅ Fast and reliable processing\n"
                f"- 🔒 Enterprise-grade security and modular pipelines\n"
                f"- ⚡ Instant response and seamless API connectivity\n\n"
                f"Let me know if you would like me to generate specific code, diagrams, or deep-dive details!"
            )
            
        prompt_tokens = len(system_prompt + user_message) // 4 + 40
        comp_tokens = len(reply) // 4 + 10
        return {
            "response": reply,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": comp_tokens,
            "latency_ms": 320,
            "provider": "smart-demo",
            "model": "smart-demo-v1"
        }

ai_engine = AIEngine()
