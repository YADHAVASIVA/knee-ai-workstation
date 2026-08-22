import pandas as pd
import numpy as np
from typing import Optional
from app.ai.oa_analysis.schemas import AnalysisStats, OAVsNonOAComparison, MaleVsFemaleComparison, AgeAnalysis

def calc_stats(series: pd.Series) -> Optional[AnalysisStats]:
    if len(series) == 0:
        return None
    return AnalysisStats(
        sample_count=len(series),
        mean_thickness=float(series.mean()),
        median_thickness=float(series.median()),
        std_thickness=float(series.std()) if len(series) > 1 else 0.0
    )

def compare_oa_groups(df: pd.DataFrame) -> Optional[OAVsNonOAComparison]:
    if df.empty:
        return None
    
    oa_df = df[df["oa_status"] == "OA"]
    non_oa_df = df[df["oa_status"] == "NON_OA"]
    
    oa_stats = calc_stats(oa_df["meniscus_thickness_pixels"])
    non_oa_stats = calc_stats(non_oa_df["meniscus_thickness_pixels"])
    
    return OAVsNonOAComparison(
        oa_stats=oa_stats,
        non_oa_stats=non_oa_stats,
        statistical_test="None (Demonstration Data)",
        p_value=None,
        conclusion="Insufficient sample size for reliable clinical statistical inference. Demonstration only."
    )

def compare_sex_groups(df: pd.DataFrame) -> Optional[MaleVsFemaleComparison]:
    if df.empty:
        return None
        
    male_df = df[df["sex"] == "Male"]
    female_df = df[df["sex"] == "Female"]
    
    return MaleVsFemaleComparison(
        male_stats=calc_stats(male_df["meniscus_thickness_pixels"]),
        female_stats=calc_stats(female_df["meniscus_thickness_pixels"])
    )

def analyze_age(df: pd.DataFrame) -> Optional[AgeAnalysis]:
    if len(df) < 2:
        return None
        
    correlation = df["age"].corr(df["meniscus_thickness_pixels"])
    
    return AgeAnalysis(
        correlation_coefficient=float(correlation) if not pd.isna(correlation) else None,
        conclusion="Statistical association observed in demonstration data. Not a clinical conclusion."
    )
