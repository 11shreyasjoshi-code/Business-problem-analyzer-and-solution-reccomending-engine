"""
Strategy Engine
───────────────
For every detected problem this engine returns:
  • Short-term quick wins  (this week / this month)
  • Long-term strategy     (1–3 months)
  • Target KPI
  • Recommended tools
"""

# ── Strategy Knowledge Base ──────────────────────────────────────────
STRATEGY_MAP = {

    "Critical Low Conversion Rate": {
        "short_term": [
            "Add trust badges (SSL, payment logos, return policy) above the fold",
            "Install a free live-chat widget (Tidio / Crisp) to help hesitant buyers",
            "Reduce checkout to 1–2 steps — remove unnecessary form fields",
            "Add urgency: 'Only 3 left!' or 'Offer ends tonight'",
            "Show at least 5 genuine customer reviews on every product page",
        ],
        "long_term": [
            "Run A/B tests on your product pages (use Google Optimize — free)",
            "Hire a UX freelancer to audit the checkout funnel",
            "Implement personalized product recommendations using Shopify apps",
            "Build a retargeting ad campaign to re-capture lost visitors",
            "Start a loyalty/rewards programme to encourage first-time buyers",
        ],
        "kpi":   "Target: Raise conversion rate from current to ≥ 2.5% within 90 days",
        "tools": ["Google Optimize", "Hotjar (free heatmaps)", "Tidio Live Chat", "Klaviyo"],
        "expected_impact": "High — even +0.5% conversion can double revenue at current traffic",
    },

    "Below-Average Conversion Rate": {
        "short_term": [
            "Improve product photography (white background, multiple angles)",
            "Rewrite product descriptions to highlight benefits, not just features",
            "Add a 'Frequently Bought Together' section to increase cart value",
            "Offer a first-purchase discount (e.g., 10% off with email sign-up)",
        ],
        "long_term": [
            "Run monthly customer surveys to find friction points",
            "Optimise mobile experience (60%+ of e-commerce traffic is mobile)",
            "Create email sequences for cart abandoners",
        ],
        "kpi":   "Target: Increase conversion rate by 0.5–1% within 60 days",
        "tools": ["Mailchimp (free tier)", "Canva (product images)", "Google PageSpeed Insights"],
        "expected_impact": "Medium — steady improvement over 2–3 months",
    },

    "Poor Marketing ROI": {
        "short_term": [
            "Pause ALL underperforming ad campaigns immediately — stop the bleeding",
            "Use UTM parameters to track exactly which ads drive real purchases",
            "Shift budget to your single best-performing channel for 30 days",
            "Negotiate better CPM/CPC rates with your current ad platforms",
        ],
        "long_term": [
            "Build organic SEO content (blog, product guides) — free long-term traffic",
            "Switch focus to email marketing (average ROI: 42x — highest of any channel)",
            "Launch a referral programme (existing customers recruit new ones for you)",
            "Test influencer micro-partnerships (10k–100k followers, cheaper & more targeted)",
        ],
        "kpi":   "Target: Achieve ≥ 3x marketing ROI within 60 days",
        "tools": ["Google Analytics 4 (free)", "SEMrush (free version)", "Mailchimp"],
        "expected_impact": "High — fixing ad spend waste has immediate financial impact",
    },

    "Inefficient Marketing Spend": {
        "short_term": [
            "Analyse which ad campaigns have the lowest cost-per-acquisition and cut others",
            "Allocate 20% of budget to test 1–2 new channels",
            "Set up Google Analytics Goals to track actual conversions from each source",
        ],
        "long_term": [
            "Develop a content marketing calendar for organic reach",
            "Build an email list — aim for 500+ subscribers in 90 days",
            "Test Google Shopping ads if you sell physical products",
        ],
        "kpi":   "Target: Reduce customer acquisition cost by 30% in 60 days",
        "tools": ["Google Analytics 4", "Facebook Ads Manager", "Mailchimp"],
        "expected_impact": "Medium — gradual improvement as you shift budget",
    },

    "Very Low Customer Retention": {
        "short_term": [
            "Send a 'We miss you' email with a 15% discount to all past customers",
            "Launch a simple loyalty programme: '5th order is free' or points system",
            "Follow up every order with a personal thank-you email within 24 hours",
            "Ask for reviews — customers who review are 3x more likely to return",
        ],
        "long_term": [
            "Set up automated email flows: welcome series, post-purchase, win-back",
            "Build a VIP tier for top 10% of customers with exclusive perks",
            "Offer subscriptions or bundles to lock in repeat purchases",
            "Conduct a Net Promoter Score (NPS) survey to find why people don't return",
        ],
        "kpi":   "Target: Increase retention rate by 10 percentage points in 90 days",
        "tools": ["Klaviyo", "LoyaltyLion", "Mailchimp", "Google Forms (NPS survey)"],
        "expected_impact": "Very High — retained customers spend 67% more than new ones",
    },

    "Moderate Customer Retention Issue": {
        "short_term": [
            "Start a monthly newsletter with value content (tips, deals, stories)",
            "Create a simple punch-card or points loyalty scheme",
            "Personalise email subject lines with the customer's first name",
        ],
        "long_term": [
            "Build post-purchase email automation in Mailchimp or Klaviyo",
            "Survey churned customers: 'What would bring you back?'",
        ],
        "kpi":   "Target: Reach 40% retention rate within 90 days",
        "tools": ["Mailchimp", "Typeform (surveys)", "Canva"],
        "expected_impact": "Medium — steady retention improvement over 2–3 months",
    },

    "Overstock / Slow Inventory Movement": {
        "short_term": [
            "Run a flash sale or bundle deal to liquidate slow-moving stock",
            "Offer free shipping on orders above a certain amount to shift inventory",
            "List excess stock on Amazon, Flipkart, or Facebook Marketplace",
            "Create 'Buy 2 Get 1 Free' promotions on overstocked items",
        ],
        "long_term": [
            "Implement a just-in-time inventory model — order smaller batches more often",
            "Use Google Trends to predict seasonal demand before ordering",
            "Negotiate consignment arrangements with suppliers to reduce holding risk",
            "Track inventory turnover per SKU monthly and discontinue slow movers",
        ],
        "kpi":   "Target: Achieve ≥ 6 inventory turns/month within 60 days",
        "tools": ["Google Sheets (inventory tracker)", "Shopify Inventory Reports", "Zoho Inventory (free)"],
        "expected_impact": "Medium — frees up cash tied in stock",
    },

    "Stockout Risk — Inventory Too Low": {
        "short_term": [
            "Place an emergency reorder for your top 5 best-selling SKUs today",
            "Add 'Back in Stock' notification buttons so you don't lose demand",
            "Temporarily pause paid ads for out-of-stock products",
            "Be transparent with customers about restock dates",
        ],
        "long_term": [
            "Calculate reorder points for every SKU (average daily sales × lead time)",
            "Find a second supplier for your top products as a backup",
            "Negotiate shorter supplier lead times or local sourcing",
            "Set up automatic low-stock alerts in your inventory system",
        ],
        "kpi":   "Target: Maintain ≥ 30 days of cover for top SKUs at all times",
        "tools": ["Zoho Inventory", "Shopify Stock Alerts", "Google Sheets"],
        "expected_impact": "High — stockouts directly kill revenue",
    },

    "High Traffic but Poor Sales Conversion": {
        "short_term": [
            "Install Hotjar (free) to watch real visitor recordings and find drop-off points",
            "Check page load speed — every 1 second delay costs 7% in conversions",
            "Make your CTA button bigger, bolder, and above the fold on every page",
            "Add a money-back guarantee badge prominently on product and checkout pages",
        ],
        "long_term": [
            "Redesign product pages based on Hotjar heatmap data",
            "Hire a CRO (Conversion Rate Optimisation) freelancer for a one-time audit",
            "Build landing pages tailored to each traffic source (ad, SEO, social)",
            "Run an ongoing A/B testing programme",
        ],
        "kpi":   "Target: Convert traffic gap — reach ≥ 2% conversion within 60 days",
        "tools": ["Hotjar (free)", "Google PageSpeed Insights", "VWO A/B Testing"],
        "expected_impact": "Very High — you already have the traffic, just fix the leaks",
    },

    "Negative Net Profit": {
        "short_term": [
            "List every expense line-by-line and cut anything non-essential immediately",
            "Raise prices by 5–10% — most customers won't notice, margin will jump",
            "Pause all paid advertising until the business is cash-flow positive",
            "Negotiate a rent/subscription discount or temporary deferral with suppliers",
        ],
        "long_term": [
            "Build a zero-based budget: justify every expense monthly",
            "Explore dropshipping to eliminate inventory holding costs",
            "Focus exclusively on your top 3 best-margin products — cut the rest",
            "Set a hard rule: marketing spend ≤ 20% of revenue",
        ],
        "kpi":   "Target: Reach break-even within 30 days, profitability within 60 days",
        "tools": ["Google Sheets (budget tracker)", "Wave (free accounting)", "Razorpay"],
        "expected_impact": "Critical — survival-level action required",
    },
}

# ── Fallback for unknown problems ────────────────────────────────────
DEFAULT_STRATEGY = {
    "short_term": [
        "Conduct a full audit of the affected area",
        "Identify the 1–2 biggest quick wins and act on them this week",
        "Set up tracking and KPI targets in a simple spreadsheet",
    ],
    "long_term": [
        "Build a 90-day improvement plan with weekly check-ins",
        "Talk to 3–5 real customers to understand their pain points",
        "Test one new approach per month and measure results",
    ],
    "kpi":   "Define and track 1 core KPI for this area per week",
    "tools": ["Google Analytics 4", "Google Sheets", "Mailchimp"],
    "expected_impact": "Varies — track weekly",
}


class StrategyEngine:
    """Maps detected problems to actionable strategies."""

    def get_strategies(self, problems: list) -> list:
        """
        Input:  list of problem dicts from ProblemDetector
        Output: same list enriched with 'strategies' key
        """
        enriched = []
        for prob in problems:
            strategy = STRATEGY_MAP.get(prob["problem"], DEFAULT_STRATEGY)
            enriched.append({**prob, "strategies": strategy})
        return enriched
