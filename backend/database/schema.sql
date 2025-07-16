-- users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- babies table  
CREATE TABLE babies (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    gender VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- activities table
CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    age_min_months INTEGER NOT NULL,
    age_max_months INTEGER NOT NULL,
    category VARCHAR(50) NOT NULL, -- motor, cognitive, social, sensory
    difficulty_level INTEGER DEFAULT 1, -- 1-5 scale
    duration_minutes INTEGER DEFAULT 15,
    materials_needed TEXT,
    instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- user_activity_interactions table
CREATE TABLE user_activity_interactions (
    id SERIAL PRIMARY KEY,
    baby_id INTEGER REFERENCES babies(id),
    activity_id INTEGER REFERENCES activities(id),
    interaction_type VARCHAR(20) NOT NULL, -- viewed, started, completed, skipped
    rating INTEGER, -- 1-5 stars if completed
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- milestones table
CREATE TABLE milestones (
    id SERIAL PRIMARY KEY,
    baby_id INTEGER REFERENCES babies(id),
    milestone_type VARCHAR(100) NOT NULL, -- first_smile, rolling_over, sitting_up
    achieved_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
