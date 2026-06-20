from datetime import datetime, date
from typing import Optional, Dict
from hijri_converter import GregorianToHijri, HijriToGregorian
import calendar


class HijriService:
    """Service for Islamic calendar operations and Hijri date conversions."""
    
    ISLAMIC_MONTHS = {
        1: "Muharram",
        2: "Safar",
        3: "Rabi al-Awwal",
        4: "Rabi al-Thani",
        5: "Jumada al-Awwal",
        6: "Jumada al-Thani",
        7: "Rajab",
        8: "Sha'ban",
        9: "Ramadan",
        10: "Shawwal",
        11: "Dhul Qa'dah",
        12: "Dhul Hijjah"
    }
    
    ISLAMIC_MONTHS_ARABIC = {
        1: "محرم",
        2: "صفر",
        3: "ربيع الأول",
        4: "ربيع الآخر",
        5: "جمادى الأولى",
        6: "جمادى الآخرة",
        7: "رجب",
        8: "شعبان",
        9: "رمضان",
        10: "شوال",
        11: "ذو القعدة",
        12: "ذو الحجة"
    }
    
    @staticmethod
    def gregorian_to_hijri(gregorian_date: date) -> str:
        """
        Convert Gregorian date to Hijri date string.
        Returns format: "23 Dhul Hijjah 1447"
        """
        hijri = GregorianToHijri(
            gregorian_date.year,
            gregorian_date.month,
            gregorian_date.day
        )
        
        month_name = HijriService.ISLAMIC_MONTHS[hijri.month]
        return f"{hijri.day} {month_name} {hijri.year}"
    
    @staticmethod
    def gregorian_to_hijri_arabic(gregorian_date: date) -> str:
        """
        Convert Gregorian date to Hijri date in Arabic.
        Returns format: "٢٣ ذو الحجة ١٤٤٧"
        """
        hijri = GregorianToHijri(
            gregorian_date.year,
            gregorian_date.month,
            gregorian_date.day
        )
        
        month_name = HijriService.ISLAMIC_MONTHS_ARABIC[hijri.month]
        return f"{hijri.day} {month_name} {hijri.year}"
    
    @staticmethod
    def hijri_to_gregorian(hijri_year: int, hijri_month: int, hijri_day: int) -> date:
        """
        Convert Hijri date to Gregorian date.
        """
        gregorian = HijriToGregorian(hijri_year, hijri_month, hijri_day)
        return date(gregorian.year, gregorian.month, gregorian.day)
    
    @staticmethod
    def get_ramadan_dates(gregorian_year: int) -> Dict[str, date]:
        """
        Get Ramadan start and end dates for a given Gregorian year.
        Returns approximate dates (actual dates depend on moon sighting).
        """
        # Ramadan is month 9 in Islamic calendar
        # Approximate calculation - actual dates require moon sighting
        ramadan_start = GregorianToHijri(gregorian_year, 3, 11)  # Approximate
        ramadan_end = GregorianToHijri(gregorian_year, 4, 9)  # Approximate
        
        return {
            "start": date(ramadan_start.year, ramadan_start.month, ramadan_start.day),
            "end": date(ramadan_end.year, ramadan_end.month, ramadan_end.day)
        }
    
    @staticmethod
    def get_dhul_hijjah_dates(gregorian_year: int) -> Dict[str, date]:
        """
        Get Dhul Hijjah dates for a given Gregorian year.
        Dhul Hijjah is month 12 in Islamic calendar.
        """
        # Approximate calculation
        dhul_hijjah_start = GregorianToHijri(gregorian_year, 6, 16)  # Approximate
        dhul_hijjah_end = GregorianToHijri(gregorian_year, 7, 15)  # Approximate
        
        return {
            "start": date(dhul_hijjah_start.year, dhul_hijjah_start.month, dhul_hijjah_start.day),
            "end": date(dhul_hijjah_end.year, dhul_hijjah_end.month, dhul_hijjah_end.day)
        }
    
    @staticmethod
    def is_ramadan(gregorian_date: date) -> bool:
        """
        Check if a given Gregorian date falls during Ramadan.
        """
        hijri = GregorianToHijri(
            gregorian_date.year,
            gregorian_date.month,
            gregorian_date.day
        )
        return hijri.month == 9
    
    @staticmethod
    def is_dhul_hijjah(gregorian_date: date) -> bool:
        """
        Check if a given Gregorian date falls during Dhul Hijjah.
        """
        hijri = GregorianToHijri(
            gregorian_date.year,
            gregorian_date.month,
            gregorian_date.day
        )
        return hijri.month == 12
    
    @staticmethod
    def get_next_charge_date_hijri(schedule_start: date, hijri_months: list[int]) -> Optional[date]:
        """
        Calculate the next charge date for a Hijri-based recurring donation.
        
        Args:
            schedule_start: The start date of the schedule
            hijri_months: List of Hijri months to charge (e.g., [9] for Ramadan)
        
        Returns:
            Next charge date or None if no upcoming date found
        """
        current_date = date.today()
        current_hijri = GregorianToHijri(
            current_date.year,
            current_date.month,
            current_date.day
        )
        
        # Check each specified Hijri month
        for month in sorted(hijri_months):
            # If the month is in the future this year
            if month > current_hijri.month:
                try:
                    next_date = HijriToGregorian(current_hijri.year, month, 1)
                    gregorian_date = date(next_date.year, next_date.month, next_date.day)
                    if gregorian_date >= schedule_start:
                        return gregorian_date
                except:
                    continue
        
        # If no month found this year, check next year
        for month in sorted(hijri_months):
            try:
                next_date = HijriToGregorian(current_hijri.year + 1, month, 1)
                gregorian_date = date(next_date.year, next_date.month, next_date.day)
                if gregorian_date >= schedule_start:
                    return gregorian_date
            except:
                continue
        
        return None
    
    @staticmethod
    def get_islamic_new_year(gregorian_year: int) -> date:
        """
        Get approximate Islamic New Year date for a given Gregorian year.
        """
        # Muharram 1 - approximate
        new_year = GregorianToHijri(gregorian_year, 7, 19)  # Approximate
        return date(new_year.year, new_year.month, new_year.day)
    
    @staticmethod
    def format_hijri_date(hijri_year: int, hijri_month: int, hijri_day: int) -> str:
        """
        Format Hijri date components into a readable string.
        """
        month_name = HijriService.ISLAMIC_MONTHS[hijri_month]
        return f"{hijri_day} {month_name} {hijri_year}"
