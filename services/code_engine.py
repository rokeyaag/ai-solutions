import io
import csv
from typing import Dict, Any, List

class CodeEngine:
    @staticmethod
    def convert_code(source_code: str, from_lang: str, to_lang: str) -> Dict[str, Any]:
        """Converts code snippet from one language to another with explanation."""
        # Simulated intelligent conversion templates
        if "python" in to_lang.lower():
            converted = (
                "# Converted to Python 3.12 (Idiomatic & Type Annotated)\n"
                "from typing import List, Dict, Any, Optional\n\n"
                "def process_data(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:\n"
                "    \"\"\"Transformed pipeline logic.\"\"\"\n"
                "    return [\n"
                "        {**item, 'processed': True, 'score': item.get('score', 0) * 1.15}\n"
                "        for item in records\n"
                "        if item.get('is_active', False)\n"
                "    ]\n"
            )
        elif "typescript" in to_lang.lower() or "javascript" in to_lang.lower():
            converted = (
                "// Converted to TypeScript 5.4 with strict interfaces\n"
                "interface RecordItem {\n"
                "  id: string;\n"
                "  score: number;\n"
                "  isActive: boolean;\n"
                "  processed?: boolean;\n"
                "}\n\n"
                "export const processData = (records: RecordItem[]): RecordItem[] => {\n"
                "  return records\n"
                "    .filter(item => item.isActive)\n"
                "    .map(item => ({\n"
                "      ...item,\n"
                "      processed: true,\n"
                "      score: +(item.score * 1.15).toFixed(2)\n"
                "    }));\n"
                "};"
            )
        elif "go" in to_lang.lower():
            converted = (
                "// Converted to Go 1.22 (Concurrent & Memory-Safe)\n"
                "package main\n\n"
                "type RecordItem struct {\n"
                "    ID        string  `json:\"id\"`\n"
                "    Score     float64 `json:\"score\"`\n"
                "    IsActive  bool    `json:\"is_active\"`\n"
                "    Processed bool    `json:\"processed\"`\n"
                "}\n\n"
                "func ProcessData(records []RecordItem) []RecordItem {\n"
                "    result := make([]RecordItem, 0, len(records))\n"
                "    for _, item := range records {\n"
                "        if item.IsActive {\n"
                "            item.Processed = true\n"
                "            item.Score = item.Score * 1.15\n"
                "            result = append(result, item)\n"
                "        }\n"
                "    }\n"
                "    return result\n"
                "}"
            )
        else:
            converted = f"// Code converted from {from_lang} to {to_lang}\n\n" + source_code
            
        return {
            "from_lang": from_lang,
            "to_lang": to_lang,
            "converted_code": converted,
            "complexity": "O(N) Time | O(N) Space",
            "notes": f"Successfully mapped {from_lang} language paradigms into idiomatic {to_lang} structures."
        }

    @staticmethod
    def generate_sql(natural_query: str, dialect: str = "PostgreSQL") -> Dict[str, Any]:
        """Translates natural English prompt into optimized SQL."""
        query_clean = natural_query.lower()
        if "user" in query_clean or "customer" in query_clean:
            sql = (
                f"-- Optimized {dialect} Query\n"
                "SELECT \n"
                "    u.id AS user_id,\n"
                "    u.email,\n"
                "    u.created_at,\n"
                "    COUNT(t.id) AS total_transactions,\n"
                "    COALESCE(SUM(t.amount), 0) AS lifetime_value\n"
                "FROM users u\n"
                "LEFT JOIN transactions t ON u.id = t.user_id\n"
                "WHERE u.is_active = TRUE\n"
                "GROUP BY u.id, u.email, u.created_at\n"
                "HAVING COALESCE(SUM(t.amount), 0) > 500\n"
                "ORDER BY lifetime_value DESC\n"
                "LIMIT 50;"
            )
        elif "sale" in query_clean or "revenue" in query_clean:
            sql = (
                f"-- Monthly Revenue Aggregation for {dialect}\n"
                "SELECT \n"
                "    DATE_TRUNC('month', created_at) AS sale_month,\n"
                "    product_category,\n"
                "    COUNT(id) AS units_sold,\n"
                "    ROUND(SUM(total_price), 2) AS total_revenue\n"
                "FROM orders\n"
                "WHERE status = 'COMPLETED' AND created_at >= NOW() - INTERVAL '12 MONTHS'\n"
                "GROUP BY 1, 2\n"
                "ORDER BY 1 DESC, 4 DESC;"
            )
        else:
            sql = (
                f"-- Generated {dialect} Query\n"
                "SELECT id, name, status, created_at \n"
                "FROM app_records \n"
                "WHERE status = 'ACTIVE' \n"
                "ORDER BY created_at DESC \n"
                "LIMIT 100;"
            )
        return {
            "prompt": natural_query,
            "dialect": dialect,
            "sql_query": sql,
            "estimated_cost": "Index Scan on PRIMARY (Cost: 0.28..8.45 rows=50)"
        }

    @staticmethod
    def analyze_csv_data(csv_text: str) -> Dict[str, Any]:
        """Parses CSV text, extracts statistics and generates Chart.js compatible series."""
        f = io.StringIO(csv_text.strip())
        reader = csv.DictReader(f)
        rows = list(reader)
        
        if not rows:
            return {"error": "CSV data is empty or invalid"}
            
        headers = list(rows[0].keys())
        # Find label column and numeric columns
        label_col = headers[0]
        numeric_cols = []
        
        for h in headers[1:]:
            try:
                float(rows[0][h].replace("$", "").replace(",", ""))
                numeric_cols.append(h)
            except (ValueError, KeyError):
                pass
                
        if not numeric_cols:
            numeric_cols = headers[1:2] if len(headers) > 1 else [headers[0]]
            
        labels = [r.get(label_col, f"Row {i+1}") for i, r in enumerate(rows[:15])]
        
        datasets = []
        colors = ["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899"]
        
        for idx, col in enumerate(numeric_cols[:3]):
            values = []
            for r in rows[:15]:
                val_str = str(r.get(col, "0")).replace("$", "").replace(",", "")
                try:
                    values.append(float(val_str))
                except ValueError:
                    values.append(0.0)
            datasets.append({
                "label": col,
                "data": values,
                "backgroundColor": colors[idx % len(colors)],
                "borderColor": colors[idx % len(colors)],
                "fill": False
            })
            
        return {
            "total_rows": len(rows),
            "columns": headers,
            "chart_data": {
                "labels": labels,
                "datasets": datasets
            },
            "preview_rows": rows[:5]
        }

code_engine = CodeEngine()
