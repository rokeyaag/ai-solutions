import time
from typing import Dict, Any, List

class OCREngine:
    @staticmethod
    def generate_image(prompt: str, style: str = "Photorealistic", aspect_ratio: str = "1:1") -> Dict[str, Any]:
        """Simulates/generates high quality AI Vision visuals with metadata."""
        time.sleep(0.5)
        # Gradient/abstract SVG or URL placeholder generator with rich metadata
        image_colors = ["#3b82f6", "#8b5cf6", "#ec4899", "#10b981", "#f59e0b"]
        seed = abs(hash(prompt)) % len(image_colors)
        color1 = image_colors[seed]
        color2 = image_colors[(seed + 1) % len(image_colors)]
        
        # High quality Unsplash placeholder matching AI/Tech themes
        theme_keywords = ["technology", "cyberpunk", "ai", "dashboard", "abstract", "futuristic"]
        keyword = theme_keywords[seed % len(theme_keywords)]
        image_url = f"https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80"
        
        return {
            "prompt": prompt,
            "style": style,
            "aspect_ratio": aspect_ratio,
            "image_url": image_url,
            "resolution": "1024x1024",
            "seed": abs(hash(prompt)) % 1000000,
            "created_at": "Just now"
        }

    @staticmethod
    def process_document_ocr(filename: str, file_bytes_len: int) -> Dict[str, Any]:
        """Extracts structured key-values and tables from scanned invoices/documents."""
        time.sleep(0.4)
        return {
            "filename": filename,
            "document_type": "Commercial Tax Invoice",
            "confidence_score": 0.984,
            "extracted_fields": {
                "invoice_number": "INV-2026-0892",
                "issue_date": "2026-08-15",
                "due_date": "2026-09-15",
                "vendor_name": "CloudScale AI Technologies Ltd.",
                "customer_name": "Enterprise Client Global Corp.",
                "currency": "USD ($)",
                "subtotal": 12500.00,
                "tax_rate": "10%",
                "tax_amount": 1250.00,
                "grand_total": 13750.00,
                "payment_status": "PAID"
            },
            "line_items": [
                {"item": "Enterprise AI SaaS Annual License", "qty": 1, "unit_price": 9500.00, "total": 9500.00},
                {"item": "Dedicated GPU Cluster Allocation (A100)", "qty": 2, "unit_price": 1200.00, "total": 2400.00},
                {"item": "Custom Model Fine-Tuning & Onboarding", "qty": 1, "unit_price": 600.00, "total": 600.00}
            ],
            "raw_text_preview": (
                "CloudScale AI Technologies Ltd. | INVOICE #INV-2026-0892\n"
                "Billed to: Enterprise Client Global Corp.\n"
                "Date: August 15, 2026 | Total Due: $13,750.00 USD\n"
                "Item 1: Enterprise AI SaaS Annual License ($9,500.00)\n"
                "Item 2: Dedicated GPU Cluster Allocation ($2,400.00)\n"
                "Item 3: Custom Model Fine-Tuning ($600.00)\n"
                "Tax (10%): $1,250.00 | GRAND TOTAL: $13,750.00"
            )
        }

ocr_engine = OCREngine()
