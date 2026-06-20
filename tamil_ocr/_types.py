from dataclasses import dataclass


@dataclass
class PageResult:
    page_num: int        # 1-based
    text: str            # OCR plain text
    char_count: int      # len(text.strip())
    is_illustration: bool  # True when char_count < illustration threshold
