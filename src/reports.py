from datetime import datetime
from typing import Any, Dict, Optional

import pandas as pd

from .logger import setup_logger

logger = setup_logger(__name__, log_file="reports")


def spending_by_category(df: pd.DataFrame, category: str, start_date: str) -> Dict[str, Any]:
    """Траты по категории"""
    try:
        # Логика фильтрации по категории и периоду
        return {"status": "success", "total": 0.0}
    except Exception as e:
        logger.error(f"Ошибка в spending_by_category: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


def spending_by_weekday(df: pd.DataFrame, date: Optional[str] = None) -> Dict[str, Any]:  # ← Исправлено: Optional[str]
    """Траты по дням недели"""
    try:
        # Обработка значения по умолчанию
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        # Логика агрегации по дням недели
        return {"status": "success", "breakdown": {}}
    except Exception as e:
        logger.error(f"Ошибка в spending_by_weekday: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


def spending_by_workday(df: pd.DataFrame, category: str, start_date: str) -> Dict[str, Any]:
    """Траты в рабочий/выходной день"""
    try:
        # Логика разделения на рабочие/выходные
        return {"status": "success", "workday": 0.0, "weekend": 0.0}
    except Exception as e:
        logger.error(f"Ошибка в spending_by_workday: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}
