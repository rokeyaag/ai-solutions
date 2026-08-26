from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from services.token_tracker import token_tracker

router = APIRouter(prefix="/api/copywriting", tags=["Copywriting & SEO Suite"])

class CopyRequest(BaseModel):
    content_type: str  # "blog_post", "cold_email", "linkedin_post", "ad_copy"
    topic: str
    target_audience: str = "B2B SaaS Founders & Tech Leaders"
    tone: str = "Professional & Persuasive"
    keywords: Optional[str] = "AI automation, SaaS growth, efficiency"

@router.post("/generate")
async def generate_copy(request: CopyRequest):
    topic = request.topic
    audience = request.target_audience
    tone = request.tone
    kw_list = [k.strip() for k in (request.keywords or "").split(",") if k.strip()]
    kw_str = ", ".join(kw_list) if kw_list else "High ROI, AI Transformation"
    
    if request.content_type == "blog_post":
        output = f"""# The Definitive Guide to {topic.title()} in 2026

**Meta Description:** Discover how {topic} is transforming operations for {audience}. Learn key strategies, tools, and actionable steps to boost ROI.
**Target Keywords:** {kw_str}  
**Tone:** {tone}

---

## Introduction: The New Paradigm
In today's hyper-competitive digital landscape, **{audience}** face unprecedented challenges in scaling workflows while preserving engineering velocity. This is precisely where **{topic}** emerges as a game changer.

## Why {topic} Matters Today
1. **Accelerated Efficiency:** Reduce manual cycle times by up to 70%.
2. **Predictable Scalability:** Eliminate operational bottlenecks through automated pipelines.
3. **Data-Driven Precision:** Empower decision-makers with real-time actionable telemetry.

## Step-by-Step Implementation Framework
* **Phase 1: Diagnostic Assessment:** Audit your current infrastructure and pinpoint friction points.
* **Phase 2: Modular Integration:** Roll out incremental solutions without disturbing legacy workflows.
* **Phase 3: Telemetry & Optimization:** Monitor key metrics ({kw_str}) to maximize return on investment.

## Conclusion & Key Takeaway
Adopting **{topic}** is no longer an optional luxury—it is the foundational prerequisite for sustainable market leadership.
"""
    elif request.content_type == "cold_email":
        output = f"""**Subject:** Quick question regarding {topic} for your team?

Hi [First Name],

I noticed your team has been scaling rapidly, and many **{audience}** we speak with are currently facing challenges around **{topic}**.

We recently helped a similar company streamline their processes, resulting in a **42% reduction in operational overhead** within 30 days.

Given your focus on **{kw_str}**, would you be open to a brief 7-minute chat this Thursday at 2 PM to explore if this could unlock similar results for you?

Best regards,  
[Your Name]  
*Growth Lead at AI SaaS Solutions*
"""
    elif request.content_type == "linkedin_post":
        output = f"""🚀 Most {audience} are approaching {topic} completely wrong.

Here is what 90% of companies do:
❌ Treat AI as a replacement rather than an amplifier
❌ Ignore proper data governance and token economics
❌ Rely on generic one-size-fits-all prompts

Here is what the top 1% do instead:
✅ Build domain-specific RAG pipelines with verified citations
✅ Automate high-friction tasks while keeping humans in the loop
✅ Track unit economics and latency with strict SLA metrics

The result? 3x operational leverage and record-low churn.

What is your biggest bottleneck with {topic} right now? Drop a comment below 👇

#AI #{request.content_type.replace('_', '')} #SaaS #FutureOfWork #{kw_list[0].replace(' ', '') if kw_list else 'Innovation'}
"""
    else:
        output = f"""### 🎯 High-Performance Ad Copy Matrix

**Headline 1 (Benefit-Led):** Master {topic.title()} in Minutes, Not Months  
**Headline 2 (Proof-Led):** Trusted by 10,000+ {audience}  
**Headline 3 (Urgency):** Scale Your Operations with Next-Gen AI Today

**Primary Text:**
Tired of wasting hours on repetitive workflows? Our comprehensive AI platform automates {topic} with enterprise security and instant setup. Join industry leaders who are saving 15+ hours every single week.

**Call To Action (CTA):** [Get Started Free — Instant Access]
"""

    token_tracker.record_usage(
        service="Copywriting & SEO",
        action=f"Generated {request.content_type.replace('_', ' ').title()} on '{topic[:25]}...'",
        prompt_tokens=180,
        completion_tokens=320,
        latency_ms=290
    )

    return {
        "content_type": request.content_type,
        "topic": topic,
        "generated_content": output,
        "tokens": 500,
        "estimated_seo_score": 94
    }
