
import sqlite3
import pandas as pd
import random
import os

BLOOM_LEVELS = ['Remember', 'Understand', 'Apply', 'Analyze', 'Evaluate', 'Create']
DIFFICULTIES = ['Easy', 'Medium', 'Hard']

DEPT_SUBJECTS = {
    'CSE': [
        'Data Structures', 'Algorithms', 'Operating Systems', 'DBMS', 'Computer Networks', 
        'Artificial Intelligence', 'Machine Learning', 'Web Development', 'Software Engineering'
    ],
    'ECE': [
        'Digital Electronics', 'Analog Circuits', 'Signals and Systems', 'Microprocessors', 
        'Communication Systems', 'VLSI Design', 'Control Systems', 'Electromagnetics'
    ],
    'ME': [
        'Thermodynamics', 'Fluid Mechanics', 'Strength of Materials', 'Manufacturing Processes', 
        'Engineering Mechanics', 'Heat Transfer', 'Machine Design', 'Automobile Engineering'
    ],
    'CE': [
        'Structural Analysis', 'Geotechnical Engineering', 'Environmental Engineering', 
        'Transportation Engineering', 'Concrete Technology', 'Surveying', 'Hydraulics'
    ],
    'EEE': [
        'Electrical Machines', 'Power Systems', 'Power Electronics', 'Circuit Theory', 
        'Electrical Measurements', 'High Voltage Engineering', 'Renewable Energy Systems'
    ]
}

# Common topics to use if specific ones aren't defined
GENERIC_TOPICS = [
    'Fundamentals', 'Advanced Concepts', 'Applications', 'System Design', 'Optimization', 
    'Integration', 'Testing', 'Simulation', 'Maintenance', 'Safety Protocols'
]

TOPICS = {
    'Data Structures': ['Arrays', 'Linked Lists', 'Trees', 'Graphs', 'Stacks', 'Queues', 'Hash Tables', 'Heaps'],
    'Algorithms': ['Sorting', 'Searching', 'Dynamic Programming', 'Greedy Algorithms', 'Recursion', 'Backtracking'],
    'Operating Systems': ['Process Management', 'Memory Management', 'File Systems', 'Deadlocks', 'Scheduling'],
    'DBMS': ['SQL', 'Normalization', 'Transactions', 'Indexing', 'NoSQL', 'ER Modelling'],
    'Digital Electronics': ['Logic Gates', 'Flip-Flops', 'Counters', 'Multiplexers', 'K-Maps'],
    'Thermodynamics': ['Laws of Thermodynamics', 'Entropy', 'Enthalpy', 'Heat Cycles', 'Refrigeration'],
    'Structural Analysis': ['Beams', 'Trusses', 'Arches', 'Cables', 'Influence Lines'],
    'Power Systems': ['Transmission', 'Distribution', 'Fault Analysis', 'Load Flow', 'Protection'],
    'Artificial Intelligence': ['Neural Networks', 'Fuzzy Logic', 'Search Algorithms', 'NLP', 'Robotics']
}

QUESTION_TEMPLATES = [
    "Explain the fundamental principles of {topic} in the context of {subject}.",
    "Differentiate between the various approaches to {topic}.",
    "Calculate the efficiency of a system designed using {topic}.",
    "Analyze the impact of {topic} on modern {subject} applications.",
    "Design a solution that effectively utilizes {topic} to solve a real-world problem.",
    "Discuss the advantages and disadvantages of {topic} in {subject}.",
    "Evaluate the performance characteristics of {topic}.",
    "How does {topic} integrate with other components in {subject}?",
    "Describe the historical evolution of {topic}.",
    "What are the critical safety considerations when dealing with {topic}?",
    "Derive the mathematical formulation for {topic}.",
    "Compare and contrast the implementation of {topic} in different scenarios."
]


def seed_database():
    db_path = os.path.join('instance', 'question_bank.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get faculty user ID
    cursor.execute("SELECT id FROM users WHERE role='Faculty'")
    faculty = cursor.fetchone()
    if not faculty:
        print("Faculty user not found. Creating default faculty user...")
        from werkzeug.security import generate_password_hash
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            ('faculty', 'faculty@example.com', generate_password_hash('faculty123'), 'Faculty')
        )
        faculty_id = cursor.lastrowid
    else:
        faculty_id = faculty[0]

    csv_file = 'sample_questions.csv'
    
    # Check if CSV exists and has data
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        print(f"Loading questions from {csv_file}...")
        try:
            df = pd.read_csv(csv_file)
            
            # Verify required columns
            required_columns = ['question_text', 'subject', 'topic', 'difficulty', 'marks', 'bloom_level', 'department']
            if not all(col in df.columns for col in required_columns):
                 print(f"CSV missing required columns: {required_columns}. Falling back to synthetic generation.")
                 # Fallthrough to synthetic generation or exit? 
                 # Better to fail safely or try to Map? 
                 # For now, let's assume if CSV exists it's valid or we error out.
                 pass

            count = 0
            for _, row in df.iterrows():
                cursor.execute('''
                    INSERT INTO questions (
                        question_text, subject, topic, difficulty, marks, 
                        bloom_level, bloom_confidence, answer, created_by, department
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['question_text'],
                    row['subject'],
                    row.get('topic', ''),
                    row.get('difficulty', 'Medium'),
                    row.get('marks', 1),
                    row.get('bloom_level', 'Remember'),
                    0.95,
                    row.get('answer', ''),
                    faculty_id,
                    row.get('department', 'CSE')
                ))
                count += 1
            
            conn.commit()
            print(f"Successfully seeded {count} questions from CSV.")
            conn.close()
            return
            
        except Exception as e:
            print(f"Error reading CSV: {e}")
            print("Falling back to synthetic generation...")

    print("Seeding database with extensive SYNTHETIC question bank...")
    total_inserted = 0

    # Generate synthetic questions for each department and subject
    for dept, subjects in DEPT_SUBJECTS.items():
        print(f"Generating questions for {dept}...")
        for subject in subjects:
            # Get topics for this subject, fall back to generic if not found
            subject_topics = TOPICS.get(subject, GENERIC_TOPICS)
            
            # Generate ~150-200 questions per subject to ensure sufficient coverage
            num_questions = random.randint(150, 200)
            
            # Bloom weights: slightly more lower-order questions as they carry fewer marks
            bloom_weights = [0.30, 0.25, 0.20, 0.15, 0.05, 0.05] 
            
            for _ in range(num_questions):
                topic = random.choice(subject_topics)
                template = random.choice(QUESTION_TEMPLATES)
                question_text = template.format(topic=topic, subject=subject)
                
                # Weighted choice for Bloom's Level
                bloom_level = random.choices(BLOOM_LEVELS, weights=bloom_weights, k=1)[0]
                
                # Smart marks assignment based on Bloom's Level
                if bloom_level in ['Remember', 'Understand']:
                    marks = random.choice([2, 3, 4, 5])
                    difficulty = 'Easy'
                elif bloom_level in ['Apply', 'Analyze']:
                    marks = random.choice([5, 6, 8, 10])
                    difficulty = 'Medium'
                else: # Evaluate, Create
                    marks = random.choice([10, 12, 15, 20])
                    difficulty = 'Hard'
                
                cursor.execute('''
                    INSERT INTO questions (
                        question_text, subject, topic, difficulty, marks, 
                        bloom_level, bloom_confidence, answer, created_by, department
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    question_text,
                    subject,
                    topic,
                    difficulty,
                    marks,
                    bloom_level,
                    0.95, # High confidence for synthetic data
                    f"Sample answer for {topic} in {subject}.",
                    faculty_id,
                    dept
                ))
                total_inserted += 1

    conn.commit()
    
    # Export to CSV for future use
    print("Exporting generated questions to sample_questions.csv...")
    try:
        df_export = pd.read_sql_query("SELECT question_text, subject, topic, difficulty, marks, bloom_level, answer, department FROM questions", conn)
        df_export.to_csv(csv_file, index=False)
        print(f"Exported {len(df_export)} questions to {csv_file}")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")

    conn.close()
    print(f"Successfully seeded {total_inserted} questions across {len(DEPT_SUBJECTS)} departments.")

if __name__ == '__main__':
    seed_database()
