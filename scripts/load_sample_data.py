# scripts/load_sample_data.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy.orm import Session
from backend.app.database import SessionLocal, engine
from backend.app.models import Base, Activity

# Create all tables
Base.metadata.create_all(bind=engine)

# Sample activities data
sample_activities = [
    {
        "title": "Tummy Time",
        "description": "Place baby on their tummy to strengthen neck and shoulder muscles",
        "age_min_months": 0,
        "age_max_months": 6,
        "category": "motor",
        "difficulty_level": 1,
        "duration_minutes": 5,
        "materials_needed": "Soft blanket",
        "instructions": "Place baby on tummy for short periods, stay close and encourage lifting head"
    },
    {
        "title": "High Contrast Cards",
        "description": "Show black and white pattern cards to stimulate vision",
        "age_min_months": 0,
        "age_max_months": 4,
        "category": "sensory",
        "difficulty_level": 1,
        "duration_minutes": 10,
        "materials_needed": "Black and white cards or pictures",
        "instructions": "Hold cards 8-12 inches from baby's face, move slowly side to side"
    },
    {
        "title": "Peek-a-Boo",
        "description": "Classic game to develop object permanence",
        "age_min_months": 4,
        "age_max_months": 12,
        "category": "cognitive",
        "difficulty_level": 2,
        "duration_minutes": 10,
        "materials_needed": "Your hands or a cloth",
        "instructions": "Cover your face or hide behind cloth, then reveal with 'peek-a-boo!'"
    },
    {
        "title": "Finger Foods Exploration",
        "description": "Let baby explore soft finger foods to develop fine motor skills",
        "age_min_months": 6,
        "age_max_months": 12,
        "category": "motor",
        "difficulty_level": 3,
        "duration_minutes": 20,
        "materials_needed": "Soft fruits, cooked vegetables",
        "instructions": "Offer small, soft pieces. Supervise closely. Let baby explore textures."
    },
    {
        "title": "Simple Stacking",
        "description": "Stack soft blocks or cups to develop hand-eye coordination",
        "age_min_months": 8,
        "age_max_months": 18,
        "category": "cognitive",
        "difficulty_level": 3,
        "duration_minutes": 15,
        "materials_needed": "Soft blocks or plastic cups",
        "instructions": "Demonstrate stacking, let baby try, celebrate attempts"
    },
    {
        "title": "Mirror Play",
        "description": "Show baby their reflection to develop self-awareness",
        "age_min_months": 2,
        "age_max_months": 8,
        "category": "social",
        "difficulty_level": 1,
        "duration_minutes": 10,
        "materials_needed": "Unbreakable mirror",
        "instructions": "Hold baby in front of mirror, point to reflection, make faces together"
    },
    {
        "title": "Baby Massage",
        "description": "Gentle massage to promote bonding and relaxation",
        "age_min_months": 0,
        "age_max_months": 24,
        "category": "social",
        "difficulty_level": 1,
        "duration_minutes": 15,
        "materials_needed": "Baby-safe oil (optional)",
        "instructions": "Use gentle strokes on arms, legs, back. Watch baby's cues for comfort"
    }
]

def load_sample_data():
    db = SessionLocal()
    try:
        # Check if activities already exist
        existing_count = db.query(Activity).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} activities. Skipping...")
            return
        
        # Add sample activities
        for activity_data in sample_activities:
            activity = Activity(**activity_data)
            db.add(activity)
        
        db.commit()
        print(f"Successfully loaded {len(sample_activities)} sample activities!")
        
        # Print summary
        print("\nActivities by category:")
        for category in ["motor", "cognitive", "sensory", "social"]:
            count = db.query(Activity).filter(Activity.category == category).count()
            print(f"  {category.capitalize()}: {count}")
            
    except Exception as e:
        print(f"Error loading data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_sample_data()
