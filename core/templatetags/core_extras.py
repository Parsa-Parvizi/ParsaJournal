from __future__ import annotations

from datetime import date, datetime
from typing import Tuple

from django import template
from django.utils import timezone, translation
from django.utils.formats import date_format

register = template.Library()

GREGORIAN_MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
JALALI_MONTH_DAYS = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
JALALI_MONTH_NAMES = [
    "فروردین",
    "اردیبهشت",
    "خرداد",
    "تیر",
    "مرداد",
    "شهریور",
    "مهر",
    "آبان",
    "آذر",
    "دی",
    "بهمن",
    "اسفند",
]
PERSIAN_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
TIME_TOKENS = set("HhGgisuaA")


def _normalize_value(value: date | datetime | None) -> date | datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        if timezone.is_aware(value):
            value = timezone.localtime(value)
        return value
    if isinstance(value, date):
        return value
    return None


def _gregorian_to_jalali(g_year: int, g_month: int, g_day: int) -> Tuple[int, int, int]:
    gy = g_year - 1600
    gm = g_month - 1
    gd = g_day - 1

    g_day_no = 365 * gy + (gy + 3) // 4 - (gy + 99) // 100 + (gy + 399) // 400
    for i in range(gm):
        g_day_no += GREGORIAN_MONTH_DAYS[i]
    if gm > 1 and ((gy + 1600) % 4 == 0 and ((gy + 1600) % 100 != 0 or (gy + 1600) % 400 == 0)):
        g_day_no += 1
    g_day_no += gd

    j_day_no = g_day_no - 79
    j_np = j_day_no // 12053
    j_day_no %= 12053

    jy = 979 + 33 * j_np + 4 * (j_day_no // 1461)
    j_day_no %= 1461

    if j_day_no >= 366:
        jy += (j_day_no - 1) // 365
        j_day_no = (j_day_no - 1) % 365

    jm = 0
    while jm < 11 and j_day_no >= JALALI_MONTH_DAYS[jm]:
        j_day_no -= JALALI_MONTH_DAYS[jm]
        jm += 1
    jd = j_day_no + 1

    return jy, jm + 1, jd


def _to_persian_digits(text: str) -> str:
    return text.translate(PERSIAN_DIGITS)


def _include_time(fmt: str | None) -> bool:
    if not fmt:
        return False
    return any(token in fmt for token in TIME_TOKENS)


def _jalali_date(value: date | datetime, include_time: bool = False) -> str:
    if isinstance(value, datetime):
        dt_value = value
        date_value = value.date()
    else:
        dt_value = None
        date_value = value

    jy, jm, jd = _gregorian_to_jalali(date_value.year, date_value.month, date_value.day)
    parts = [str(jd), JALALI_MONTH_NAMES[jm - 1], str(jy)]
    result = " ".join(parts)

    if include_time and dt_value is not None:
        result = f"{result}, {dt_value.strftime('%H:%M')}"

    return _to_persian_digits(result)


@register.filter
def localized_date(value: date | datetime | None, fmt: str = "F d, Y") -> str:
    normalized = _normalize_value(value)
    if normalized is None:
        return ""

    current_lang = (translation.get_language() or "en").split("-")[0]

    if current_lang == "fa":
        return _jalali_date(normalized, include_time=_include_time(fmt))

    with translation.override(current_lang or "en"):
        return date_format(normalized, fmt)


@register.filter
def localized_number(value: int | float | str | None) -> str:
    if value is None:
        return ""
    text = str(value)
    current_lang = (translation.get_language() or "en").split("-")[0]
    if current_lang == "fa":
        return _to_persian_digits(text)
    return text


@register.simple_tag
def language_label(lang_code: str | None) -> str:
    lang_code = (lang_code or "").lower()
    current_lang = (translation.get_language() or "en").split("-")[0]

    if current_lang == "fa":
        return "فارسی" if lang_code == "fa" else "English"

    return lang_code.upper()


@register.filter
def localized_site_name(value: str | None) -> str:
    """Return site name localized for current language."""
    default_en = "Parsa Journal"
    default_fa = "پارسا ژورنال"
    current_lang = (translation.get_language() or "en").split("-")[0]
    name = (value or "").strip()

    if current_lang == "fa":
        if not name or name.lower() == default_en.lower():
            return default_fa
        return name

    return name or default_en


# Translation dictionary for common category and tag names
CATEGORY_TRANSLATIONS = {
    # Article categories
    "Technology": "فناوری",
    "Science": "علم",
    "Culture": "فرهنگ",
    "Politics": "سیاست",
    "Literature": "ادبیات",
    "History": "تاریخ",
    "Philosophy": "فلسفه",
    "Art": "هنر",
    "Music": "موسیقی",
    "Film": "سینما",
    "Books": "کتاب‌ها",
    "Reviews": "نقدها",
    "Opinion": "نظر",
    "News": "اخبار",
    "Lifestyle": "سبک زندگی",
    # Book categories
    "Fiction": "داستان",
    "Non-Fiction": "غیرداستان",
    "Biography": "زندگینامه",
    "Memoir": "خاطرات",
    "Poetry": "شعر",
    "Drama": "نمایشنامه",
    "Classic": "کلاسیک",
    "Contemporary": "معاصر",
    "Mystery": "رمان جنایی",
    "Thriller": "هیجان‌انگیز",
    "Romance": "عاشقانه",
    "Fantasy": "فانتزی",
    "Science Fiction": "علمی-تخیلی",
    "Horror": "وحشت",
    # Movie categories
    "Action": "اکشن",
    "Comedy": "کمدی",
    "Drama": "درام",
    "Romance": "عاشقانه",
    "Thriller": "هیجان‌انگیز",
    "Horror": "وحشت",
    "Sci-Fi": "علمی-تخیلی",
    "Documentary": "مستند",
    "Animation": "انیمیشن",
    "Crime": "جنایی",
    "Adventure": "ماجراجویی",
}

TAG_TRANSLATIONS = {
    "Book Review": "نقد کتاب",
    "Movie Review": "نقد فیلم",
    "Article": "مقاله",
    "Analysis": "تحلیل",
    "Review": "نقد",
    "Recommendation": "پیشنهاد",
    "Discussion": "بحث",
    "Opinion": "نظر",
    "News": "اخبار",
    "Culture": "فرهنگ",
    "Literature": "ادبیات",
    "Film": "سینما",
    "Books": "کتاب‌ها",
    "Reading": "خواندن",
    "Writing": "نوشتن",
    "Thoughts": "افکار",
    "Reflection": "تأمل",
    # Additional common tags
    "Society": "جامعه",
    "Innovation": "نوآوری",
    "Business": "کسب‌وکار",
    "Environment": "محیط زیست",
    "Health": "سلامت",
    "Education": "آموزش",
    "AI": "هوش مصنوعی",
    "Economy": "اقتصاد",
    "Art": "هنر",
    "Technology": "فناوری",
    "Science": "علم",
    "Politics": "سیاست",
    "History": "تاریخ",
}


@register.filter
def translate_name(name: str | None) -> str:
    """Translate category/tag names to Persian if current language is Persian"""
    if not name:
        return ""
    
    current_lang = (translation.get_language() or "en").split("-")[0]
    
    if current_lang == "fa":
        # Check category translations first
        if name in CATEGORY_TRANSLATIONS:
            return CATEGORY_TRANSLATIONS[name]
        # Check tag translations
        if name in TAG_TRANSLATIONS:
            return TAG_TRANSLATIONS[name]
        # If no translation found, return original
        return name
    
    return name


@register.filter
def get_model_name(obj) -> str:
    """Get the model name of an object"""
    if obj is None:
        return ""
    return obj.__class__.__name__

