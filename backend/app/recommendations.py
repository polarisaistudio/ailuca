from sqlalchemy.orm import Session
from datetime import datetime, date
from .models import Activity, Baby

def calculate_age_in_months(birth_date: date) -> int:
    """Calculate baby's age in months"""
    today = datetime.now().date()
    months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
    return max(0, months)

def get_recommendations(baby: Baby, db: Session, limit: int = 10):
    """Get age-appropriate activity recommendations for a baby"""
    
    age_months = calculate_age_in_months(baby.birth_date)
    
    # Simple rule-based recommendations
    # Get activities suitable for baby's age (+/- 2 months for flexibility)
    suitable_activities = db.query(Activity).filter(
        Activity.age_min_months <= age_months + 2,
        Activity.age_max_months >= age_months - 2
    ).all()
    
    # Simple scoring algorithm
    scored_activities = []
    for activity in suitable_activities:
        score = calculate_activity_score(activity, age_months)
        scored_activities.append({
            "activity": activity,
            "score": score,
            "reason": get_recommendation_reason(activity, age_months)
        })
    
    # Sort by score and return top recommendations
    scored_activities.sort(key=lambda x: x["score"], reverse=True)
    return scored_activities[:limit]

def calculate_activity_score(activity: Activity, baby_age_months: int) -> float:
    """Calculate recommendation score for an activity"""
    score = 1.0
    
    # Perfect age match gets highest score
    age_diff = abs((activity.age_min_months + activity.age_max_months) / 2 - baby_age_months)
    if age_diff == 0:
        score += 2.0
    elif age_diff <= 1:
        score += 1.5
    elif age_diff <= 2:
        score += 1.0
    
    # Prefer easier activities for younger babies
    if baby_age_months < 6:
        score += (6 - activity.difficulty_level) * 0.2
    
    # Prefer shorter activities for very young babies
    if baby_age_months < 3 and activity.duration_minutes <= 10:
        score += 0.5
    
    return score

def get_recommendation_reason(activity: Activity, baby_age_months: int) -> str:
    """Generate explanation for why this activity is recommended"""
    reasons = []
    
    if activity.age_min_months <= baby_age_months <= activity.age_max_months:
        reasons.append("Perfect age match")
    else:
        reasons.append("Good for developing skills")
    
    if activity.category == "motor":
        reasons.append("Builds physical development")
    elif activity.category == "cognitive":
        reasons.append("Enhances brain development")
    elif activity.category == "social":
        reasons.append("Improves social skills")
    elif activity.category == "sensory":
        reasons.append("Stimulates senses")
    
    return " • ".join(reasons)
