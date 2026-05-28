"""
LLM Explainer
─────────────
Generates a natural-language explanation of the analysis results.

Priority:
  1. HuggingFace Inference API  (if HF_API_TOKEN is set in .env)
  2. Smart template fallback     (works without any API key)
"""

import os
import requests

# Load .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")

# Model to use — Mistral 7B Instruct (free on HuggingFace)
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"


# ── HuggingFace Call ─────────────────────────────────────────────────
def _call_huggingface(prompt: str) -> str | None:
    """Calls the HuggingFace Inference API. Returns text or None on failure."""
    if not HF_API_TOKEN or HF_API_TOKEN == "your_huggingface_token_here":
        return None  # No token → skip to fallback

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens":  600,
            "temperature":     0.7,
            "return_full_text": False,
        },
    }
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and result:
                return result[0].get("generated_text", "").strip()
        return None
    except Exception:
        return None


# ── Build the prompt ─────────────────────────────────────────────────
def _build_prompt(data: dict, problems: list, strategies: list) -> str:
    biz     = data.get("business_name", "the business")
    biz_type= data.get("business_type", "e-commerce")
    sales   = data.get("monthly_sales", 0)
    traffic = data.get("website_traffic", 0)
    conv    = data.get("conversion_rate", 0)
    ret     = data.get("retention_rate", 0)
    mkt     = data.get("marketing_spend", 0)

    prob_lines = "\n".join(
        f"- {p['problem']} (Confidence: {p['confidence']}%): {p['detail']}"
        for p in problems
    ) if problems else "- No major problems detected."

    strat_lines = "\n".join(
        f"- For '{s['problem']}': "
        + (s['strategies']['short_term'][0] if s['strategies']['short_term'] else '')
        for s in strategies
    )

    prompt = f"""<s>[INST]
You are a friendly, expert e-commerce business consultant.
Analyse the following business data and write a clear, encouraging, human-like paragraph (200–300 words) that:
1. Acknowledges the current situation honestly but constructively
2. Explains WHY the identified problems are happening in plain English
3. Highlights the MOST important action the owner should take first
4. Ends with an encouraging note about the business's potential

Business: {biz} ({biz_type})
Monthly Sales: ₹{sales:,}
Website Traffic: {traffic:,} visitors/month
Conversion Rate: {conv}%
Customer Retention: {ret}%
Marketing Spend: ₹{mkt:,}/month

Problems Detected:
{prob_lines}

Top Recommended Actions:
{strat_lines}

Write the analysis in a warm, direct, professional tone — like a consultant talking to the owner face-to-face.
Do NOT use bullet points. Write continuous paragraphs only.
[/INST]"""

    return prompt


# ── Smart Template Fallback ──────────────────────────────────────────
def _template_explanation(data: dict, problems: list) -> str:
    """
    Generates a solid explanation without any API.
    Reads the actual metrics and builds meaningful sentences.
    """
    biz     = data.get("business_name", "Your business")
    sales   = data.get("monthly_sales", 0)
    traffic = data.get("website_traffic", 0)
    conv    = data.get("conversion_rate", 0)
    ret     = data.get("retention_rate", 0)
    mkt     = data.get("marketing_spend", 0)
    spend   = max(mkt, 1)
    roi     = round(sales / spend, 1)

    if not problems:
        return (
            f"{biz} is performing well across all major metrics. "
            f"With a {conv}% conversion rate and {ret}% retention rate, "
            "your fundamentals are solid. Focus on scaling what's already working — "
            "increase traffic through SEO and content marketing, and double down on your "
            "best-performing marketing channel. Keep monitoring your inventory levels "
            "to avoid stockouts as you grow."
        )

    high_probs = [p for p in problems if p["severity"] == "High"]
    med_probs  = [p for p in problems if p["severity"] == "Medium"]

    parts = []

    # Opening
    total = sales
    parts.append(
        f"{biz} is currently generating ₹{total:,} per month with "
        f"{traffic:,} visitors and a {conv}% conversion rate."
    )

    # Traffic vs conversion analysis
    if traffic > 2000 and conv < 2.0:
        parts.append(
            f"The biggest opportunity is right in front of you: you are already attracting "
            f"{traffic:,} visitors every month, but only {conv}% of them are buying. "
            "This gap — known as a conversion problem — is extremely common in e-commerce "
            "and is almost always fixable. The likely culprits are: a confusing checkout "
            "process, lack of customer trust signals, or slow page load speed."
        )
    elif conv >= 2.5:
        parts.append(
            f"Your {conv}% conversion rate is solid — you are turning visitors into buyers "
            "better than most stores. That is a real strength to build on."
        )

    # Marketing ROI
    if roi < 2.5:
        parts.append(
            f"On the marketing side, you are spending ₹{mkt:,}/month but generating "
            f"only {roi}x return. For every rupee you invest, you should be making at "
            f"least ₹3 back. Right now you are not there. The priority fix is to stop "
            "spending on what isn't working and redirect budget to channels that convert."
        )
    elif roi >= 3.5:
        parts.append(
            f"Your marketing ROI of {roi}x is impressive — you are getting good value "
            "from your ad spend. Consider increasing your budget in your best channels."
        )

    # Retention
    if ret < 30:
        parts.append(
            f"Customer retention at {ret}% means you are losing the majority of buyers "
            "after their first purchase. This is expensive — getting a new customer costs "
            "5× more than keeping one. A simple email sequence after every purchase, "
            "combined with a loyalty programme, can move this number quickly."
        )

    # Priority action
    if high_probs:
        first_fix = high_probs[0]["problem"]
        parts.append(
            f"If you can only fix one thing right now, focus on: '{first_fix}'. "
            "Address this first before spending on anything else."
        )

    # Closing encouragement
    parts.append(
        "The good news: every problem identified here has a clear, proven solution. "
        "E-commerce businesses at your stage improve dramatically with just 2–3 focused "
        "changes. Start this week, measure after 30 days, and adjust. You've got this."
    )

    return " ".join(parts)


# ── Public API ───────────────────────────────────────────────────────
def generate_explanation(data: dict, problems: list, strategies: list) -> str:
    """
    Main function called by app.py.
    Tries HuggingFace first; falls back to smart template.
    """
    prompt = _build_prompt(data, problems, strategies)
    hf_result = _call_huggingface(prompt)

    if hf_result and len(hf_result) > 100:
        return hf_result

    # Fallback — always works
    return _template_explanation(data, problems)

# ── Explainer Class Wrapper ─────────────────────────────────────────
class Explainer:
    """Wrapper class for the explanation generation functionality."""
    
    def generate_explanation(self, data: dict, problems: list, strategies: list) -> str:
        """
        Generates a natural-language explanation of the analysis results.
        Tries HuggingFace API first, falls back to smart template.
        """
        return generate_explanation(data, problems, strategies)