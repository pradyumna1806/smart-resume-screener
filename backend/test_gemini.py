import asyncio

from app.services.llm_service import extract_candidate_profile

sample_resume = """
PRADYUMNA MARUDHURI \nAmaravathi, India  |  +91 6281080339  |  marudhuripradyumna@gmail.com \nLinkedIn  |  GitHub \nPROFESSIONAL SUMMARY \nComputer Science undergraduate at VIT-AP (2027), pursuing a parallel B.S. in Data Science and Applications at IIT Madras. Strong \nfundamentals in Data Structures and Algorithms, with experience in building full-stack applications, REST APIs, databases, and AI-enabled \nsystems. Skilled in AI/ML, NLP, RAG, and Generative AI using Python, Java, SQL, FastAPI, and Flask, with exposure to AWS cloud architecture \nand scalable system design.  \nEDUCATION \nVIT-AP University - B.Tech in Computer Science \n2027 | CGPA: 8.61/10 \nRelevant Coursework : Database Management Systems (DBMS), Object-Oriented Programming (OOPs), Operating Systems, \nComputer Networks \nIIT Madras - B.S. in Data Science and Applications \nOngoing | Diploma in Programming completed \nSKILLS \nLanguages & Data : Python, Java, SQL, Data Structures and Algorithms \nAI & Machine Learning: Scikit-learn, PyTorch, Hugging Face, RAG, Generative AI  \nBackend & Systems: Flask, FastAPI, REST APIs, System Design  \nFrontend: Vue.js, React.js, Next.js  \nCloud & Tools: AWS, PostgreSQL, MongoDB, Git/GitHub \nPROJECTS \nTimed Quiz & Assessment System   \nCourse Project, Modern Application Development II, IIT Madras | Python, Flask, Vue.js, SQLite, Redis, Celery, REST APIs, JWT  \n●​ Built a full-stack quiz platform with role-based authentication, timed assessments, automated scoring, and performance analytics.  \n●​ Developed REST APIs with Redis caching and Celery-powered background jobs for scheduled reports, reminders, and CSV exports.  \n●​ Designed a secure backend with JWT authentication and optimized API performance using caching and asynchronous task \nexecution.   \nLifeDesk – AI-Powered Personal Administrative Assistant  \nPersonal Project | Flutter, FastAPI, PostgreSQL, ChromaDB, Google Gemini API, OCR, JWT  \n●​ Designed an AI-powered personal administrative assistant for managing documents, tasks, reminders, bills, and personal \ninformation within a unified application.  \n●​ Implemented OCR-based document extraction with semantic search, retrieval, and intelligent task automation through a \nmulti-agent AI architecture.  \n●​ Delivered a full-stack system with secure JWT authentication, PostgreSQL persistence, vector-based retrieval, and cloud-ready REST \nAPIs.  \nCERTIFICATIONS \n●​ MongoDB Associate Database Administrator | MongoDB | 2026 \n●​ AWS Academy Cloud Foundations & Cloud Architecting | Amazon Web Services | 2025 \n●​ Diploma in Programming | IIT Madras | 2026 \n●​ Git & GitHub - Online Workshop Certificate | IIT Madras | 2026 \n●​ HackerRank Software Engineer Intern Certificate | HackerRank | 2026 \nLEADERSHIP & EXTRACURRICULARS \nResearch Team Lead | NGC Club, VIT-AP \n●​ Led a 10-member research team, coordinated 2 hackathons, and mentored junior members on research topic selection and project \nscoping  \n●​ Led inter-college outreach for VTAPP, VIT-AP’s annual technical fest, engaging with students across multiple colleges during two \neditions.   \nCODING PROFILES \nHackerRank (5★ Java, 2★ SQL)  |  Leetcode (106+ problems solved)  |  Kaggle
"""

async def main():
    profile = await extract_candidate_profile(sample_resume)

    print(profile.model_dump_json(indent = 2))

if __name__ == "__main__":
    asyncio.run(main())

    

