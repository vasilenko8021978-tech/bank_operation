import re
from typing import Any, Dict, List

from .logger import setup_logger

logger = setup_logger(__name__, log_file="services")


def get_cashback_categories(year: int, month: int, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Выгодные категории повышенного кешбэка"""
    try:
        # Исправлено: добавлена аннотация типа для переменной
        categories: Dict[str, float] = {}  # ← КРИТИЧЕСКИ ВАЖНО: аннотация типа

        # Логика расчёта кешбэка
        for tx in transactions:
            # Извлекаем категорию
            category = ""
            for key, value in tx.items():
                if isinstance(key, str) and key.strip() == "description":
                    category = str(value).strip()
                    break

            if category:
                # Упрощённый расчёт (в реальном проекте — сложная логика)
                categories[category] = categories.get(category, 0.0) + 1.0

        return {"status": "success", "categories": categories}
    except Exception as e:
        logger.error(f"Ошибка в get_cashback_categories: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


def get_invest_piggybank(month: int, transactions: List[Dict[str, Any]], round_limit: float) -> Dict[str, Any]:
    """Инвесткопилка"""
    try:
        total = 0.0
        # Логика расчёта округления
        return {"status": "success", "total": total}
    except Exception as e:
        logger.error(f"Ошибка в get_invest_piggybank: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


def simple_search(query: str, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Простой поиск"""
    try:
        results = [tx for tx in transactions if query.lower() in str(tx).lower()]
        return {"status": "success", "count": len(results), "results": results}
    except Exception as e:
        logger.error(f"Ошибка в simple_search: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


def phone_number_search(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Поиск по телефонным номерам"""
    try:
        pattern = re.compile(r"\+?\d[\d\-\(\) ]{9,}\d")
        results = []
        for tx in transactions:
            desc = str(tx.get("description", ""))
            if pattern.search(desc):
                results.append(tx)
        return {"status": "success", "count": len(results), "results": results}
    except Exception as e:
        logger.error(f"Ошибка в phone_number_search: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


def person_transfer_search(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Поиск переводов физическим лицам"""
    try:
        keywords = ["физическое лицо", "физлицо", "человек", "индив"]
        results = []
        for tx in transactions:
            desc = str(tx.get("description", "")).lower()
            if any(kw in desc for kw in keywords):
                results.append(tx)
        return {"status": "success", "count": len(results), "results": results}
    except Exception as e:
        logger.error(f"Ошибка в person_transfer_search: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}
