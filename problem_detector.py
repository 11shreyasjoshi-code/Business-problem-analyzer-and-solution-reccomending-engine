"""
Problem Detector — Core ML Module
─────────────────────────────────
Analyses the business metrics entered by the user and identifies
problems with confidence scores.  Uses benchmark thresholds that
are calculated from real industry data for e-commerce.
"""

class ProblemDetector:
    """
    Detects problems in an e-commerce business by comparing the
    user's metrics against industry benchmarks.
    """

    # ── Industry Benchmarks ─────────────────────────────────────────
    BENCHMARKS = {
        "conversion_rate": {
            "critical": 1.0,   # Below this → critical problem
            "low":      2.0,   # Below this → medium problem
            "ideal":    2.5,   # Industry average
            "unit":     "%",
        },
        "marketing_roi": {
            "critical": 1.5,
            "low":      2.5,
            "ideal":    3.5,
            "unit":     "x",
        },
        "retention_rate": {
            "critical": 15.0,
            "low":      30.0,
            "ideal":    40.0,
            "unit":     "%",
        },
        "inventory_turnover": {
            "critical_low":  2.0,   # Too much stock
            "critical_high": 15.0,  # Stockout risk
            "ideal":         8.0,
            "unit":          "turns/month",
        },
    }

    # ────────────────────────────────────────────────────────────────
    def _derived_metrics(self, data: dict) -> dict:
        """
        Calculate extra metrics from raw user input so we have more
        signals to work with.
        """
        sales   = data.get("monthly_sales", 0)
        spend   = max(data.get("marketing_spend", 1), 1)   # avoid /0
        traffic = max(data.get("website_traffic", 1), 1)
        inv     = max(data.get("inventory_level", 1), 1)

        daily_sales = sales / 30.0 if sales else 0

        return {
            "marketing_roi":       round(sales / spend, 2),
            "traffic_to_sales":    round(sales / traffic, 4),
            "inventory_turnover":  round(daily_sales * 30 / inv, 2),
            "net_profit":          sales - spend - data.get("operating_cost", 0),
            "profit_margin":       round(
                (sales - spend - data.get("operating_cost", 0)) / max(sales, 1) * 100, 1
            ),
        }

    # ── Confidence calculation ───────────────────────────────────────
    @staticmethod
    def _confidence(deviation_pct: float, base: int = 60, cap: int = 95) -> int:
        """
        The further a metric deviates from its benchmark,
        the more confident we are that it is a real problem.
        deviation_pct: how far below benchmark as a percentage (0–100+)
        """
        score = base + deviation_pct * 0.4
        return int(min(cap, max(base, score)))

    # ── Main detection method ────────────────────────────────────────
    def detect(self, data: dict) -> tuple[list, dict]:
        """
        Returns (problems_list, derived_metrics_dict)
        Each problem dict has:
            problem, severity, confidence, icon,
            your_value, benchmark, metric, detail
        """
        derived  = self._derived_metrics(data)
        problems = []

        conv  = data.get("conversion_rate", 0)
        roi   = derived["marketing_roi"]
        ret   = data.get("retention_rate", 0)
        inv_t = derived["inventory_turnover"]
        traffic = data.get("website_traffic", 0)

        # ── 1. Conversion Rate ─────────────────────────────────────
        if conv < self.BENCHMARKS["conversion_rate"]["critical"]:
            dev = ((self.BENCHMARKS["conversion_rate"]["critical"] - conv)
                   / self.BENCHMARKS["conversion_rate"]["critical"]) * 100
            problems.append({
                "problem":    "Critical Low Conversion Rate",
                "severity":   "High",
                "confidence": self._confidence(dev, 70, 95),
                "icon":       "🔴",
                "your_value": f"{conv}%",
                "benchmark":  f"{self.BENCHMARKS['conversion_rate']['ideal']}%",
                "metric":     "conversion_rate",
                "detail":     (
                    f"Your conversion rate ({conv}%) is critically below the "
                    f"industry average of {self.BENCHMARKS['conversion_rate']['ideal']}%. "
                    "Most visitors are leaving without buying."
                ),
            })
        elif conv < self.BENCHMARKS["conversion_rate"]["low"]:
            dev = ((self.BENCHMARKS["conversion_rate"]["low"] - conv)
                   / self.BENCHMARKS["conversion_rate"]["low"]) * 100
            problems.append({
                "problem":    "Below-Average Conversion Rate",
                "severity":   "Medium",
                "confidence": self._confidence(dev, 60, 85),
                "icon":       "🟡",
                "your_value": f"{conv}%",
                "benchmark":  f"{self.BENCHMARKS['conversion_rate']['ideal']}%",
                "metric":     "conversion_rate",
                "detail":     (
                    f"Your conversion rate ({conv}%) is below the industry average. "
                    "Small improvements here can significantly boost revenue."
                ),
            })

        # ── 2. Marketing ROI ───────────────────────────────────────
        if roi < self.BENCHMARKS["marketing_roi"]["critical"]:
            dev = ((self.BENCHMARKS["marketing_roi"]["critical"] - roi)
                   / self.BENCHMARKS["marketing_roi"]["critical"]) * 100
            problems.append({
                "problem":    "Poor Marketing ROI",
                "severity":   "High",
                "confidence": self._confidence(dev, 65, 93),
                "icon":       "🔴",
                "your_value": f"{roi}x",
                "benchmark":  f"{self.BENCHMARKS['marketing_roi']['ideal']}x",
                "metric":     "marketing_roi",
                "detail":     (
                    f"For every ₹1 you spend on marketing you earn only ₹{roi}. "
                    f"The target is ₹{self.BENCHMARKS['marketing_roi']['ideal']}. "
                    "You are losing money on ads."
                ),
            })
        elif roi < self.BENCHMARKS["marketing_roi"]["low"]:
            dev = ((self.BENCHMARKS["marketing_roi"]["low"] - roi)
                   / self.BENCHMARKS["marketing_roi"]["low"]) * 100
            problems.append({
                "problem":    "Inefficient Marketing Spend",
                "severity":   "Medium",
                "confidence": self._confidence(dev, 58, 82),
                "icon":       "🟡",
                "your_value": f"{roi}x",
                "benchmark":  f"{self.BENCHMARKS['marketing_roi']['ideal']}x",
                "metric":     "marketing_roi",
                "detail":     (
                    f"Your marketing ROI ({roi}x) is below the ideal {self.BENCHMARKS['marketing_roi']['ideal']}x. "
                    "Budget reallocation could improve this quickly."
                ),
            })

        # ── 3. Customer Retention ──────────────────────────────────
        if ret < self.BENCHMARKS["retention_rate"]["critical"]:
            dev = ((self.BENCHMARKS["retention_rate"]["critical"] - ret)
                   / self.BENCHMARKS["retention_rate"]["critical"]) * 100
            problems.append({
                "problem":    "Very Low Customer Retention",
                "severity":   "High",
                "confidence": self._confidence(dev, 68, 92),
                "icon":       "🔴",
                "your_value": f"{ret}%",
                "benchmark":  f"{self.BENCHMARKS['retention_rate']['ideal']}%",
                "metric":     "retention_rate",
                "detail":     (
                    f"Only {ret}% of your customers return. Acquiring new customers "
                    "costs 5x more than retaining existing ones — this is a profitability killer."
                ),
            })
        elif ret < self.BENCHMARKS["retention_rate"]["low"]:
            dev = ((self.BENCHMARKS["retention_rate"]["low"] - ret)
                   / self.BENCHMARKS["retention_rate"]["low"]) * 100
            problems.append({
                "problem":    "Moderate Customer Retention Issue",
                "severity":   "Medium",
                "confidence": self._confidence(dev, 58, 82),
                "icon":       "🟡",
                "your_value": f"{ret}%",
                "benchmark":  f"{self.BENCHMARKS['retention_rate']['ideal']}%",
                "metric":     "retention_rate",
                "detail":     (
                    f"Your retention rate ({ret}%) is below the recommended {self.BENCHMARKS['retention_rate']['ideal']}%. "
                    "A loyalty programme or email campaign could help."
                ),
            })

        # ── 4. Inventory Turnover ──────────────────────────────────
        if inv_t < self.BENCHMARKS["inventory_turnover"]["critical_low"]:
            problems.append({
                "problem":    "Overstock / Slow Inventory Movement",
                "severity":   "Medium",
                "confidence": 78,
                "icon":       "🟡",
                "your_value": f"{inv_t} turns/mo",
                "benchmark":  f"{self.BENCHMARKS['inventory_turnover']['ideal']} turns/mo",
                "metric":     "inventory_turnover",
                "detail":     (
                    f"Your inventory turns over only {inv_t}x/month against the ideal "
                    f"{self.BENCHMARKS['inventory_turnover']['ideal']}x. "
                    "Cash is tied up in unsold stock."
                ),
            })
        elif inv_t > self.BENCHMARKS["inventory_turnover"]["critical_high"]:
            problems.append({
                "problem":    "Stockout Risk — Inventory Too Low",
                "severity":   "High",
                "confidence": 85,
                "icon":       "🔴",
                "your_value": f"{inv_t} turns/mo",
                "benchmark":  f"{self.BENCHMARKS['inventory_turnover']['ideal']} turns/mo",
                "metric":     "inventory_turnover",
                "detail":     (
                    f"Your stock is turning {inv_t}x/month, which is very fast. "
                    "You are at high risk of running out of stock and losing sales."
                ),
            })

        # ── 5. Traffic vs Conversion Gap ──────────────────────────
        if traffic > 2000 and conv < 1.5:
            problems.append({
                "problem":    "High Traffic but Poor Sales Conversion",
                "severity":   "High",
                "confidence": 88,
                "icon":       "🔴",
                "your_value": f"Conv: {conv}%",
                "benchmark":  "Conv: 2.5%",
                "metric":     "traffic_conversion_gap",
                "detail":     (
                    f"You have good traffic ({traffic:,} visitors) but only {conv}% convert. "
                    "This usually means a UX, trust, or pricing problem on the site."
                ),
            })

        # ── 6. Profit sanity check ────────────────────────────────
        net = derived["net_profit"]
        if net < 0:
            problems.append({
                "problem":    "Negative Net Profit",
                "severity":   "High",
                "confidence": 99,
                "icon":       "🔴",
                "your_value": f"₹{net:,}",
                "benchmark":  "> ₹0",
                "metric":     "net_profit",
                "detail":     (
                    f"After marketing spend and operating costs your business is losing "
                    f"₹{abs(net):,} per month. Immediate cost control is needed."
                ),
            })

        return problems, derived
